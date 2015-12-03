#!/usr/local/bin/env python
import scipy.cluster.hierarchy as sch
import numpy as np
import gensim.models
from config import get_word2vec_model

model = None

def word2vec_sims(terms):
  global model
  if model is None:
    f = get_word2vec_model()
    model = gensim.models.Word2Vec.load(f)
  b = []
  for w in terms:
    a = []
    for v in terms:
      a.append(model.similarity(w,v))
    b.append(a)
  return np.matrix(b)

def cluster_suggestions(suggestions_dict):
  t = suggestions_dict.keys()
  c = sch.fcluster(sch.linkage(word2vec_sims(t)),t=0.5,criterion="inconsistent")
  for i in range(0,len(suggestions_dict.keys())):
    term = t[i]
    suggestions_dict[term] = { 
      'weight': suggestions_dict[term], 
      'cluster': c[i]
    }
  return suggestions_dict