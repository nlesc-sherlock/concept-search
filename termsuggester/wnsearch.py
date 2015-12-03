#!/usr/bin/env python

import nltk
from nltk.corpus import wordnet as wn

# This method requires to run dw_wordnet prior to any execution with this suggester

class WNSearch():
    """Class to perform searches in WordNet"""
    def suggest_terms(self,query_word):
        term_dict={}
        for syn in wn.synsets(query_word):
            term_dict[syn._name.split('.')[0]]=1
            for hyp in syn.hypernyms():
                term_dict[hyp._name.split('.')[0]]=1
        return term_dict
