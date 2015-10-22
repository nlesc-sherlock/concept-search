#!/usr/bin/env python
################################################################################
#    Created by Oscar Martinez                                                 #
#    o.rubi@esciencecenter.nl                                                  #
################################################################################

# Import a Document Corpus in JSON to ElasticSearch and creates the index

import sys
from elasticsearch import Elasticsearch

def fillES(inputDir):
    es = Elasticsearch()
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
    for p in os.listdir(inputDir):
        with open(os.path.join(inputDir), 'r') as f:
            data = f.read()
    
        es.bulk(index='enron', doc_type='email', body=data, request_timeout=20)
    
if __name__ == '__main__':
    fillES(sys.argv[1])