#!/usr/bin/env python

# run ./bin/elasticsearch in the directory where you installed it

from elasticsearch import Elasticsearch
es = Elasticsearch()
import os

class ELSearch():
    """Class to perform searches with Elastic Search"""
    def suggest_terms(self,query_word):
        query = {
            "query": {
                "query_string": {
                    "query": query_word
                }
            },
            "aggregations" : {
                "significantTerms" : {
                    "significant_terms" : { "field" : "text", "size": 15 }
                }
            }
        }
        res = es.search(index='enron', doc_type='email', body=query, size=0)
        term_dict={}
        for b in res['aggregations']['significantTerms']['buckets']:
            term_dict[b['key']] = b['score']
        return term_dict
