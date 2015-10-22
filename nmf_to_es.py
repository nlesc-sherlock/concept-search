#!/usr/bin/env python

# Push NMF results to Elasticsearch.

import json
import sys

from elasticsearch import Elasticsearch

components = json.load(open(sys.argv[1]))

# Skip the largest component, it's probably the background component.
largest = max((i for i in range(len(components))),
              key=lambda j: len(components[j]))

es = Elasticsearch()

for component in components:
    # Get only the top-100 terms. Output from nmf.py is sorted in ascending
    # order of weight.
    terms = [term for term, _ in component[-100:]]
    if len(terms) == 0:
        continue

    es.index('suggestions', 'cluster', body={"terms": ' '.join(terms)})
