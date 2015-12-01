// Term suggestion by mutual information:
// http://www.iro.umontreal.ca/~nie/IFT6255/carpineto-Survey-QE.pdf, p. 14
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math"
	"net/http"
	"os"
	"runtime"
	"sort"
	"strings"
	"sync"
)

func main() {
	if len(os.Args) < 3 {
		fmt.Fprintf(os.Stderr, "usage: %s index doctype\n", os.Args[0])
		os.Exit(1)
	}
	index, doctype := os.Args[1], os.Args[2]

	nworkers := runtime.GOMAXPROCS(0)

	docs := make(chan hit, nworkers)
	go allDocs(index, doctype, docs)

	stats := pairStats(nworkers, docs)
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

	for ts := range output {
		fmt.Printf("%q: ", ts.term)
		for _, tc := range ts.top {
			fmt.Printf(" %q %f", tc.term, tc.count)
		}
		fmt.Println("")
	}
}

// Compute co-occurrence statistics.
func pairStats(nworkers int, docs <-chan hit) map[string]termStats {
	var wg sync.WaitGroup
	wg.Add(nworkers)

	ch := make(chan map[string]termStats)

	// Collect term and term pair statistics from ES.
	for i := 0; i < nworkers; i++ {
		go func() {
			stats := make(map[string]termStats)
			for h := range docs {
				tokens := analyze(h.Source.Text)
				for i := range tokens {
					if tokens[i].Type == "<ALPHANUM>" {
						ti := tokens[i].Token
						si := stats[ti]
						si.count++
						if si.coocc == nil {
							si.coocc = make(map[string]float64)
						}
						for j := i; j < len(tokens) && j < i+windowsize; j++ {
							if tokens[j].Type == "<ALPHANUM>" {
								tj := tokens[j].Token
								si.coocc[tj]++
							}
						}
						stats[ti] = si
					}
				}
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
			tk.count += v.count
			if tk.coocc == nil {
				tk.coocc = make(map[string]float64)
			}
			for other, n := range v.coocc {
				tk.coocc[other] += n
			}
			total[k] = tk
		}
	}
	return total
}

// Get top-k terms by mutual information.
func topMI(ts *termWithStats, global map[string]termStats,
	nterms, npairs float64, k int) *termTopK {

	coocc := make([]termCount, 0, len(ts.stats.coocc))
	for other, count := range ts.stats.coocc {
		if other != ts.term {
			coocc = append(coocc, termCount{term: other, count: count})
		}
	}

	probI := ts.stats.count / nterms
	for j := range coocc {
		probJ := global[coocc[j].term].count / nterms
		probCo := coocc[j].count / npairs
		mi := math.Log1p(probCo / (probI * probJ))

		coocc[j].count = mi
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

type termStats struct {
	count float64
	coocc map[string]float64
}

type termWithStats struct {
	term  string
	stats termStats
}

type termTopK struct {
	term string
	top  []termCount
}

type termCount struct {
	term  string
	count float64
}

type byCount []termCount

func (a byCount) Len() int           { return len(a) }
func (a byCount) Less(i, j int) bool { return a[i].count > a[j].count }
func (a *byCount) Swap(i, j int)     { (*a)[i], (*a)[j] = (*a)[j], (*a)[i] }

const (
	esbase     = "http://localhost:9200"
	windowsize = 4
)

// JSON parser.
type searchresult struct {
	hits     `json:"hits"`
	ScrollId string `json:"_scroll_id"`
	//Timed_out bool `json:"timed_out"`
	//Took int `json:"took"`
}

type hits struct {
	Hits []hit `json:"hits"`
}

type hit struct {
	Id     string `json:"_id"`
	Source doc    `json:"_source"`
}

type doc struct {
	Text string `json:"text"`
}

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

		var result searchresult
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

type tokens struct {
	Tokens []token `json:"tokens"`
}

type token struct {
	Type  string `json:"type"`
	Token string `json:"token"`
}

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

	var t tokens
	err = json.Unmarshal(data, &t)
	if err != nil {
		panic(err)
	}

	return t.Tokens
}
