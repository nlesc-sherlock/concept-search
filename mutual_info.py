#!/usr/bin/env python

# Generates, for each term in the input collection, the top-K related terms by
# mutual information.

from __future__ import print_function
import os
import os.path
import sys

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

# Max_features chosen to keep memory usage down.
cv = CountVectorizer(input='filename', binary=True, max_df=.95, min_df=5,
                     max_features=10000, dtype=np.float64)

try:
    K, basedir = sys.argv[1:]
    K = int(K)
except Exception:
    print("usage: %s K dir\nTo get top-K MI terms for all files in dir"
          % sys.argv[0], file=sys.stderr)
    sys.exit(1)


def all_files():
    for person in os.listdir(basedir):
        docs_dir = os.path.join(basedir, person, 'all_documents')
        for f in os.listdir(docs_dir):
            yield os.path.join(docs_dir, f)


X = cv.fit_transform(all_files())

prior = X.mean(axis=0)     # 1/P(u)
cooccur = (X.T * X).toarray()   # P(u, v)

# log(P(u, v) / (P(u)*P(v)) + 1)
np.log1p(cooccur, out=cooccur)
cooccur /= prior
cooccur /= prior.T

vocab = np.asarray(sorted(cv.vocabulary_.keys(), key=cv.vocabulary_.get),
                   dtype=object)

for term, row in zip(vocab, cooccur):
    greatest = np.argpartition(row, len(row) - K)[-K:]
    best_terms = vocab[greatest]
    print(term, " ".join(best_terms))
