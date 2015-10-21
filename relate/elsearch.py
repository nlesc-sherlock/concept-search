#!/usr/bin/env python

# run ./bin/elasticsearch in the directory where you installed it

from elasticsearch import Elasticsearch
es = Elasticsearch()
import os

class ELSearch():
    """Class to perform searches with Elastic Search"""
    def __init__(self,dump_dir=None, initialize=False):
        if initialize:
            config = {}
            config['settings'] = {
                'analysis' : {
                'analyzer': {
                    'default': {
                        'type':'standard',
                        'stopwords': '_english_',
                    }
                }
                }
            }

            config['mappings'] = { 
                'email': {
                'properties': {
                    'text': {
                        'type': 'string', 
                        'term_vector': 'with_positions_offsets_payloads'
                    },
                }
                }
            }
            es.indices.create(index='enron', body=config)

            # index data
            for p in os.listdir(dump_dir):
                with open(os.path.join(dump_dir, p), 'r') as f:
                    data = f.read()

                es.bulk(index='enron', doc_type='email', body=data, request_timeout=20)

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
