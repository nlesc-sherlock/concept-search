from elasticsearch import Elasticsearch
import elasticsearch.exceptions
from elasticsearch.helpers import scan


class PrecomputedSuggester(object):
    """Term suggester that serves pre-computed suggestions."""
    # Used for mutual information, but reusable. Index format is one document
    # per term, with the term as the _id, that contains a list of
    # {"term": term, "value": weight} structures.

    def __init__(self, index_name="mi"):
        self._es = Elasticsearch()
        self._index_name = index_name

    def suggest_terms(self, query_word):
        try:
            hit = self._es.get(index=self._index_name, doc_type='miterm',
                               id=query_word)
            return {t["term"]: t["value"] for t in hit['_source']['terms']}
        except elasticsearch.exceptions.NotFoundError:
            return {}


class PrecomputedClusterSuggester(object):
    """Term suggester that uses precomputed term clusters."""
    # In practice, this class serves NMF term cluster results, but it can be
    # reused for anything that serves similar results.

    def __init__(self):
        # XXX Make this configurable.
        self._es = Elasticsearch()

    def suggest_terms(self, query_word):
        terms = set()
        for hit in scan(self._es, query=_make_query(query_word),
                        index='suggestions', doc_type='cluster'):
            terms.update(hit['_source']['terms'].split())
        # We should keep the weights around, but currently we don't.
        return {term: 1.0 for term in terms}


def _make_query(term):
    return {"query": {"term": {"terms": {"value": term}}}}

