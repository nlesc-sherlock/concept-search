#!/usr/bin/env python

# run ./bin/elasticsearch in the directory where you installed it
import os, urllib2, json, operator
from elasticsearch import Elasticsearch
import vsmlib


es = Elasticsearch()


class RocchioSuggester():
    """Class to get suggestions using Relevance Feedback (Rocchio algorithm)"""
    def __init__(self, numResults = 20, numTop = 20, numBottom = 20, weightInitial = 1., weightTop = 1., weightBottom = 1.):
        self.numResults = numResults
        self.numTop = numTop
        self.numBottom = numBottom
        self.weightInitial = weightInitial
        self.weightTop = weightTop
        self.weightBottom = weightBottom
    
    def centroid(self, xs):
        ks = set([])
        for x in xs: 
            for k in x: 
                ks.add(x)
        c = {}
        for k in ks:
            v = 0
            n = 0
            for x in xs:
                if k in x:
                    n += 1
                    v += x[k]
            c[k] = v / k
        return c
    
    def getTVsCentroid(self, esresponse):
        tvs = []
        if 'hits' in esresponse and 'hits' in esresponse['hits']:
            for i in range(esresponse['hits']['hits']):
                #data = es.termvectors(index='enron', doc_type='email', id=esresponse['hits']['hits'][i]['_id'])
                data = json.load(urllib2.urlopen('http://localhost:9200/enron/email/' + esresponse['hits']['hits'][i]['_id'].replace('/','%2F') + '/_termvector'))
                tv = {}
                for k in data['term_vectors']['text']['terms']:
                    tv[k] = data['term_vectors']['text']['terms'][k]['term_freq']
                tvs.append(tv)
        return self.centroid(tvs)
    
    def suggest_terms(self, query_word):
        queryTop = {
            "query": {"query_string": {"query": query_word}}
        }
        queryBottom = {
            "query": {"query_string": {"query": query_word}},
            "sort": {"_score": { "order": "asc" }}
        }
        resTop = es.search(index='enron', doc_type='email', body=queryTop, size=self.numTop)
        resBottom = es.search(index='enron', doc_type='email', body=queryBottom, size=self.numBottom)
        
        initialTV = {query_word : 1.}
        
        centroidTop = self.getTVsCentroid(resTop)
        centroidBottom = self.getTVsCentroid(resBottom)
        
        normCentroidTop = {}
        maxDimCentroidTop = float(max(centroidTop.values()))
        for k in centroidTop:
            normCentroidTop[k] = float(centroidTop[k]) / maxDimCentroidTop
            
        normCentroidBottom = {}
        maxDimCentroidBottom = float(max(centroidBottom.values()))
        for k in centroidBottom:
            normCentroidBottom[k] = float(centroidBottom[k]) / maxDimCentroidBottom
            
        ks = set(initialTV.values() + normCentroidTop.values() + normCentroidBottom.values())
        finalTV = {}
        for k in ks:
            finalTV[k] = (self.weightInitial * initialTV.get(k, 0)) + (self.weightTop * normCentroidTop.get(k, 0)) - (self.weightBottom * normCentroidBottom.get(k, 0))
        
        return dict(sorted(finalTV.items(), key=operator.itemgetter(1))[:self.numResults])
