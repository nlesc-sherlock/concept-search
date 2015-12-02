// Term suggestion by mutual information:
// http://www.iro.umontreal.ca/~nie/IFT6255/carpineto-Survey-QE.pdf, p. 14
//
// Fetches documents from Elasticsearch and writes them back into a custom
// index.
//
// Implementation notes: mutual information between terms t and u is
// log1p(P(t,u) / (P(t)×P(u))). P(t,u) is the relative frequency with which
// t and u co-occur within a window; P(t,u) = P(u,t).
package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"math"
	"net/http"
	"os"
	"runtime"
	"sort"
	"strings"
	"sync"
)

var miIndex = flag.String("index", "mi",
	"name of MI terms index")
var windowsize = flag.Int("w", 4,
	"size of window for determining co-occurrence")

func main() {
	flag.Parse()
	args := flag.Args()
	if len(args) < 2 {
		fmt.Fprintf(os.Stderr, "usage: %s index doctype\n", os.Args[0])
		os.Exit(1)
	}
	index, doctype := args[0], args[1]

	nworkers := runtime.GOMAXPROCS(0)

	docs := make(chan hit, nworkers)
	go allDocs(index, doctype, docs)

	stats := cooccurStats(nworkers, docs)
	nterms, npairs := 0., 0.
	for _, s := range stats {
		nterms += s.count
		for _, count := range s.coocc {
			npairs += count
		}
	}

	ch := make(chan *termWithStats, nworkers)
	output := make(chan *termTopK, nworkers)

	var wg sync.WaitGroup
	wg.Add(nworkers)
	for i := 0; i < nworkers; i++ {
		go func() {
			for ts := range ch {
				output <- topMI(ts, stats, nterms, npairs, 20)
			}
			wg.Done()
		}()
	}

	go func() {
		wg.Wait()
		close(output)
	}()

	go func() {
		for term, stat := range stats {
			ch <- &termWithStats{term, stat}
		}
		close(ch)
	}()

	store(output)
}

// Compute co-occurrence statistics.
//
// Consumes all documents coming in on the channel docs; uses nworkers
// goroutines.
// Returns, for each term occurring in docs, a termStats.
func cooccurStats(nworkers int, docs <-chan hit) map[string]termStats {
	var wg sync.WaitGroup
	wg.Add(nworkers)

	ch := make(chan map[string]termStats)

	// Collect term and term pair statistics from ES.
	for i := 0; i < nworkers; i++ {
		go func() {
			stats := make(map[string]termStats)
			for h := range docs {
				cooccur(analyze(h.Text), stats)
			}
			ch <- stats
			wg.Done()
		}()
	}

	go func() {
		wg.Wait()
		close(ch)
		println("got all co-occurrence statistics")
	}()

	total := <-ch
	for st := range ch {
		for k, v := range st {
			tk := total[k]
			tk.init()
			tk.count += v.count
			for other, n := range v.coocc {
				tk.coocc[other] += n
			}
			total[k] = tk
		}
	}
	return total
}

// Add co-occurrence statistics for tokens to stats.
func cooccur(tokens []token, stats map[string]termStats) {
	for i := range tokens {
		if tokens[i].Type == "<ALPHANUM>" {
			ti := tokens[i].Token
			si := stats[ti]
			si.init()
			si.count++
			for j := i; j < len(tokens) && j < i+*windowsize; j++ {
				if tokens[j].Type == "<ALPHANUM>" {
					tj := tokens[j].Token
					si.coocc[tj]++
				}
			}
			stats[ti] = si
		}
	}
}

// Get top-k terms by mutual information for ts.term.
func topMI(ts *termWithStats, global map[string]termStats,
	nterms, npairs float64, k int) *termTopK {

	coocc := make([]termCount, 0, len(ts.coocc))
	for other, count := range ts.coocc {
		if other != ts.term {
			coocc = append(coocc, termCount{Term: other, Count: count})
		}
	}

	probI := ts.count / nterms
	for j := range coocc {
		probJ := global[coocc[j].Term].count / nterms
		probCo := coocc[j].Count / npairs
		mi := math.Log1p(probCo / (probI * probJ))

		coocc[j].Count = mi
	}

	bycount := byCount(coocc)
	sort.Sort(&bycount)

	return &termTopK{term: ts.term, top: bycount[:min(k, len(bycount))]}
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

// Statistics for a term (which is not represented in this struct).
type termStats struct {
	count float64            // Frequency of the term in the collection.
	coocc map[string]float64 // Terms that co-occur with the term.
}

func (t *termStats) init() {
	if t.coocc == nil {
		t.coocc = make(map[string]float64)
	}
}

// Like termStats, but actually represents the term.
type termWithStats struct {
	term string
	termStats
}

type termTopK struct {
	term string
	top  []termCount
}

type termCount struct {
	Term  string  `json:"term"`
	Count float64 `json:"value"`
}

// Sorts a []termCount by descending count.
type byCount []termCount

func (a byCount) Len() int           { return len(a) }
func (a byCount) Less(i, j int) bool { return a[i].Count > a[j].Count }
func (a *byCount) Swap(i, j int)     { (*a)[i], (*a)[j] = (*a)[j], (*a)[i] }

const esbase = "http://localhost:9200"

type hit struct {
	Id  string `json:"_id"`
	doc `json:"_source"`
}

type doc struct {
	Text string `json:"text"`
}

// Fetches from Elasticsearch all documents of type doctype in the given index.
// Produces its results on the channel docs.
func allDocs(index, doctype string, docs chan<- hit) {
	defer close(docs)
	u := fmt.Sprintf("%s/%s/%s/_search?scroll=10s&size=100",
		esbase, index, doctype)
	postdata := `{"sort": ["_doc"]}`

	nhits := 0

	for {
		resp, err := http.Post(u, "application/json",
			strings.NewReader(postdata))
		if err != nil {
			panic(err)
		}

		data, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			panic(err)
		}

		type hits struct {
			Hits []hit `json:"hits"`
		}
		var result struct {
			hits     `json:"hits"`
			ScrollId string `json:"_scroll_id"`
			//Timed_out bool `json:"timed_out"`
			//Took int `json:"took"`
		}
		err = json.Unmarshal(data, &result)
		if err != nil {
			panic(err)
		}

		if len(result.hits.Hits) == 0 { // End of scroll.
			break
		}

		for _, h := range result.hits.Hits {
			docs <- h
		}
		nhits += len(result.hits.Hits)
		fmt.Fprintln(os.Stderr, nhits)

		u = esbase + "/_search/scroll?scroll=1m"
		postdata = result.ScrollId
	}
}

type token struct {
	Type  string `json:"type"`
	Token string `json:"token"`
}

// Analyze s by passing it to Elasticsearch.
func analyze(s string) []token {
	u := esbase + "/_analyze"
	resp, err := http.Post(u, "text", strings.NewReader(s))
	if err != nil {
		panic(err)
	}

	data, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		panic(err)
	}

	var t struct {
		Tokens []token `json:"tokens"`
	}
	err = json.Unmarshal(data, &t)
	if err != nil {
		panic(err)
	}

	return t.Tokens
}

const chunksize = 100

// Store all of terms in Elasticsearch.
func store(terms chan *termTopK) {
	bulk := make(chan *bytes.Buffer, 1)
	go func() {
		chunk := new(bytes.Buffer)

		n := 0
		for t := range terms {
			writeBulk(t, chunk)

			n++
			if n == chunksize {
				bulk <- chunk
				n = 0
				chunk = new(bytes.Buffer)
			}
		}
		if n > 0 {
			bulk <- chunk
		}
		close(bulk)
	}()

	u := esbase + "/_bulk"
	for chunk := range bulk {
		resp, err := http.Post(u, "application/x-www-form-urlencoded", chunk)

		var data []byte
		if err == nil {
			data, err = ioutil.ReadAll(resp.Body)
		}
		if err != nil {
			fmt.Fprintf(os.Stderr, "got %s for %s\n", data, chunk)
			panic(err)
		}
	}
}

// Write t as ES bulk requests to w.
func writeBulk(t *termTopK, w io.Writer) {
	jt, _ := json.Marshal(t.term)
	fmt.Fprintf(w,
		`{"index": {"_index": %q, "_type": "miterm", "_id": %s}}`,
		*miIndex, jt)
	fmt.Fprintln(w)

	fmt.Fprint(w, "{\"terms\":")
	jt, _ = json.Marshal(t.top)
	fmt.Fprintf(w, "%s}\n", jt)
}
