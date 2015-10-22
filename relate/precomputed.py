from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan


class PrecomputedSuggester(object):
    def __init__(self):
        # XXX Make this configurable.
        self._es = Elasticsearch()

    def suggest_terms(self, query_word):
        terms = set()
        for hit in scan(self._es, query=_make_query(query_word),
                        index='suggestions', doc_type='cluster'):
            terms.update(hit['_source']['terms'].split())
        # We should keep the weights around, but currently we don't.
        return [(term, 1.0) for term in terms]


def _make_query(term):
    return {"query": {"term": {"terms": {"value": term}}}}
