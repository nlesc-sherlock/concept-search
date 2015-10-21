#!/usr/bin/env python

import nltk

class WNSearch():
    """Class to perform searches in WordNet"""
    def __init__(self,datadir=None,initialize=False):
        if initialize:
            nltk.download('wordnet', download_dir=datadir)
        if type(datadir) == str and datadir not in nltk.data.path:
            nltk.data.path.append(datadir)

    def suggest_terms(self,query_word):
        from nltk.corpus import wordnet as wn
        term_dict={}
        for syn in wn.synsets(query_word):
            term_dict[syn._name.split('.')[0]]=1
            for hyp in syn.hypernyms():
                term_dict[hyp._name.split('.')[0]]=1
        return term_dict