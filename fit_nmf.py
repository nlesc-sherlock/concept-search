#!/usr/bin/env python

# Fits an NMF (non-negative matrix factorization) model to a document
# corpus and reports the components ("topics") found.
#
# The idea is to then index the components as documents.
#
# The first argument controls the number of components. More components
# means fewer non-zero terms per component, but more computation time
# required to fit the model.
#
# The second argument is the regularization weight. Higher values press
# values to zero more aggressively.

# Generates, for each term in the input collection, the top-K related terms by
# mutual information.

from __future__ import print_function
import json
from operator import itemgetter
import os
import os.path
import sys

import numpy as np
from sklearn.decomposition import non_negative_factorization
from sklearn.feature_extraction.text import TfidfVectorizer

try:
    n_components, alpha, basedir, outfile = sys.argv[1:]
    alpha = float(alpha)
    n_components = int(n_components)
except Exception:
    print("usage: %s n_components alpha dir outfile"
          % sys.argv[0], file=sys.stderr)
    sys.exit(1)


def all_files():
    for person in os.listdir(basedir):
        docs_dir = os.path.join(basedir, person, 'all_documents')
        for f in os.listdir(docs_dir):
            yield os.path.join(docs_dir, f)


def pretty(components, vocab):
    for i, c in enumerate(components):
        # Remove all too minor components to get an ever sparser model.
        nz = np.where(c > 1e-6)
        print(len(nz[0]), "terms in component", i)
        yield sorted(zip(vocab[nz], c[nz]), key=itemgetter(1))


# Max_features chosen to keep memory usage down.
print("Constructing term-document matrix")
tv = TfidfVectorizer(input='filename', sublinear_tf=True, max_df=.90, min_df=5,
                     max_features=20000, stop_words='english',
                     token_pattern='[a-z]{2,}')
X = tv.fit_transform(all_files())

print("Fitting NMF model")
_, components, _ = non_negative_factorization(X, n_components=n_components,
                                              l1_ratio=1., alpha=alpha,
                                              max_iter=15, tol=1e-3, verbose=1,
                                              regularization='components')

vocab = np.asarray(sorted(tv.vocabulary_.keys(), key=tv.vocabulary_.get),
                   dtype=object)

print("Dumping output")
with open(outfile, "w") as out:
    json.dump(list(pretty(components, vocab)), out)
