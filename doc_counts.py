from __future__ import print_function
from itertools import count

from elasticsearch import Elasticsearch


def get_top_terms(es, index, doc_type, field, n=1000):
    """Get the top-n terms from index/doc_type/field by document count.

    Document counts are approximate and tend to be underestimates due to the
    funny ways of Elasticsearch [1]. The bottom of the ranking especially
    should not be trusted.

    Parameters
    ----------
    es : Elasticsearch
    index : string
    doc_type : string
    field : string
    n : integer
        Maximum number of terms to return.

    Returns
    -------
    term_counts : list of tuple
        A list of (term, doc_count) pairs.

    References
    ----------
    [1] https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html#search-aggregations-bucket-terms-aggregation-approximate-counts
    """
    query = {
        "size": 0,
        "aggs": {
            "terms_by_doc_count": {"terms": {"field": field, "size": n}}
        }
    }
    result = es.search(index=index, doc_type=doc_type, body=query)
    buckets = result["aggregations"]["terms_by_doc_count"]["buckets"]
    return [(bucket["key"], bucket["doc_count"]) for bucket in buckets]


def get_all_terms(es, index, doc_type, field):
    """Get all terms in index/doc_type/field and their counts.

    See get_terms for usage.
    """
    # Dirty hack up ahead.
    for i in count():
        n = 10 ** i
        terms = get_terms(es, index, doc_type, field, n=n)
        if len(terms) < n:
            return terms


if __name__ == '__main__':
    terms = get_all_terms(Elasticsearch(), index='enron', doc_type='email',
                          field='text')
    for t, count in terms:
        print(t, count)
