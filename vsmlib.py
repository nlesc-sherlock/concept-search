# Tiny library of utility functions for the vector space model.
# Represent vectors as string -> term count mappings.

from math import sqrt


def cosine(x, y):
    return dot(x, y) / (norm(x) * norm(y))


def norm(x):
    return sqrt(sum(f ** 2 for f in x.values()))


def dot(x, y):
    return sum(x[k] * y.get(k, 0) for k in x)
