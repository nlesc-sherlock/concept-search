#!/usr/bin/env python

# Term suggestion based on NMF. This is kind of experimental.

from __future__ import print_function
from collections import defaultdict
from operator import itemgetter
import os
import os.path

import numpy as np
from sklearn.decomposition import non_negative_factorization as nmf
from sklearn.feature_extraction.text import TfidfVectorizer


class NMFSuggester(object):
    """Term suggestion based on NMF.

    Fits an L1-regularized NMF (non-negative matrix factorization) model to a
    term-document matrix (w/ tf-idf weights). In each component, the terms
    with non-zero weight will become suggestions for all other terms in the
    component.

    Parameters
    ----------
    basedir : string
        Path to directory holding the corpus.
        XXX Document the format here.

    n_components : integer, optional
        Number of components in NM Fmodel. More components should mean fewer
        non-zero terms per component, but more computation time required to fit
        the model.

    alpha : float, optional
        Regularization strength. Larger values press more terms to zero weight.

    max_terms : int
        Maximum number of terms to consider in term-document matrix. Terms are
        selected by their document frequency.

    remove_largest : boolean, optional
        Whether to remove the largest component (the one with the most non-zero
        terms). This is typically a "background" component capturing all the
        common terms from the corpus.

    The first argument controls the number of components. More components
    means fewer non-zero terms per component, but more computation time
    required to fit the model.
    """
    def __init__(self, basedir, n_components=500, alpha=1., max_terms=20000,
                 remove_largest=True):

        print("Constructing term-document matrix")
        tv = TfidfVectorizer(input='filename', sublinear_tf=True, max_df=.90,
                             min_df=5, max_features=max_terms,
                             stop_words='english', token_pattern='[a-z]{2,}')
        X = tv.fit_transform(_all_files(basedir))

        print("Fitting NMF model")
        _, components, _ = nmf(X, n_components=n_components, l1_ratio=1.,
                               alpha=alpha, max_iter=10, tol=1e-2, verbose=1,
                               regularization='components')

        if remove_largest:
            largest = np.argmax((components > 0).sum(axis=1))
        else:
            largest = -1

        vocab = sorted(tv.vocabulary_.keys(), key=tv.vocabulary_.get)
        vocab = np.asarray(vocab, dtype=object)

        components = _to_dict(components, vocab, largest)
        suggestions = defaultdict(list)
        for component in components:
            for term, _ in component:
                # TODO de-duplicate
                suggestions[term] += component

        self._suggestions = suggestions

    def suggest_terms(self, query_term):
        return self._suggestions[query_term]


def _all_files(basedir):
    for person in os.listdir(basedir):
        docs_dir = os.path.join(basedir, person, 'all_documents')
        for f in os.listdir(docs_dir):
            yield os.path.join(docs_dir, f)


def _to_dict(components, vocab, largest):
    for i, c in enumerate(components):
        # Remove all too minor components to get an ever sparser model.
        nz = np.where(c > 1e-6)
        if len(nz[0]) > 0 and i != largest:
            print(len(nz[0]), "terms in component", i)
            yield sorted(zip(vocab[nz], c[nz]), key=itemgetter(1))
