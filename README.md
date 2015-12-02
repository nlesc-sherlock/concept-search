# Concept Search for Exploratory Data Analysis

This repository contains a python package, a web server and a web front-end to find suggestions to words which are being queried in a document store.

## Planning/Subtasks

* Make list of test queries (single term vs multiple terms/phrase queries)
  * Papers etc. about Enron data: http://enrondata.org/content/research/
* Implement query expansion algorithms
* Merge/cluster results from query expansion algorithms
* Visualize merged query expansion results
* Build simple user interface/demo
* Do the same for terms that do not correlate/co-occur with query terms (does
  that make sense?)

## Installation

Several python packages have to installed for the various comnponents of this repository.

pandas Flask Flask-cors nltk vincent elasticsearch sklearn scipy gensim

## termsuggester

The termsuggester python package contains a pipeline to use different methods to find suggestions for a term.
The pipeline uses several term-search methods to get suggestions. The term-search methods are configured and instanciated by the user.
The suggestions from the various term-search methods are aggregated. The aggregation method can be selected by the user.

Current term-search methods:
 - ELSearch: Find suggestions using ElasticSearch significant terms aggregation from a Document Corpus.
 - WNSearch: Use WordNet to find suggestions for a term
 - PrecomputedClusterSuggester: Finds suggesstions using a pre-computed term clustering data set stored in ElasticSearch. The term clustering data set is computed with Non-negative matrix factorization (NMF) clustering method.
 - Word2VecSuggester: Use word2vec to find most similar terms

Current methods for aggregation of results from various term-search methods:
 - Sum
 - Average

To add a new term-search method you need to create a class which only condition is to have a suggest_terms(query_word) method.
This method must return a suggestion set which is a Python dictionary in the form of:
{str : float, str : float, ...}
where str is a suggested term and float is the weight of the suggestion (how relevant it is)

The search-term methods may use other applications such as ElasticSearch. In the package we assume that such applications have been properly set up.
For example that the related ElasticSearch indixes have been created.

### Method set up

- ELSearch method requires to run `get_dc.py` and `dc_to_es.py` before using termsuggester.
- WNSearch method does not require setup.
- PrecomputedClusterSuggester method requires to run `fit_nmf.py` and `nmf_to_es.py` before using termsuggester.
To get NMF word clusters for suggestions, run
    `pip install -U git+https://github.com/scikit-learn/scikit-learn.git`
Then
    `python fit_nmf.py <n_clusters> <alpha> nmf_output.json`
(Try `n_clusters`=500 and `alpha`=1.)
Then store the result in Elasticsearch:
    `python nmf_to_es.py nmf_output.json`
The index that is constructed can then be used by the PrecomputedClusterSuggester.

- Word2VecSuggester requires to run `train_word2vec.py` before using it.

### Example of usage (after various methods setup)

```
from TermSuggestionsAggregator import TermSuggestionsAggregator, Aggregation
from elsearch import ELSearch
from wnsearch import WNSearch
from precomputed import PrecomputedClusterSuggester

methods = (WNSearch(), ELSearch(), PrecomputedClusterSuggester())
ts = TermSuggestionsAggregator()
d = ts.getSuggestions('car', methods, Aggregation.Average)
print d
```

## webserver

## webdemo

1. Have Elasticsearch running. Elasticsearch must have an `enron` index
   containing the enron emails (and optionally precomputed term suggestions).
2. Have the webserver running: `python webserver/webTermSuggester.py`.
3. Run the webdemo

    cd webdemo
    gulp serve

## Data

* [Get the data](https://github.com/nlesc-sherlock/concept-search/blob/develop/GettingTheData.ipynb)
(IPython notebook)

## Related documentation

* [Text feature extraction using scikit-learn](http://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)
* Given a term-document matrix _A_ (where cell _t_, _d_ contains the weight of term _t_ in document _d_),
the term-term correlation matrix is _A_*_A_.T (see
[Automatic Query Expansion in Information Retrieval](http://www-labs.iro.umontreal.ca/~nie/IFT6255/carpineto-Survey-QE.pdf),
page 13, above equation 5).

## More ideas (for next sprint)

### Ontologies

* [A review of ontology based query expansion](https://nlesc.sharepoint.com/sites/sherlock/Shared%20Documents/papers/concept%20search/1-s2.0-S0306457306001476-main.pdf)
* [IBM Watson Concept Expansion](http://concept-expansion-demo.mybluemix.net/)
  * The Concept Expansion process is also known as Semantic Lexicon Induction
  or Semantic Set Expansion.
  * Probably a more 'ontology based' approach
  * Could not find a paper about the IBM Watson Concept Expansion Webservice
