#!/usr/bin/env python
################################################################################
#    Created by Oscar Martinez                                                 #
#    o.rubi@esciencecenter.nl                                                  #
################################################################################

class Method:
    ElasticSearch, WordNet = range(2)

class ConceptSuggester:
    """Class used to get suggestions from a concept"""
    def __init__(self):
        return 
    
    def getSuggestions(self, concept, method = [Method.ElasticSearch, Method.WordNet]):
        """Get suggestions to a term.
        The method parameter indicates which methods are used to get suggestions.
        method parameter can be a single value or a list of values. Use the Method class to specify a method to be used
        By default all available methods are used."""
        # Check that concept is a string and a single word
        if type(concept) != str:
            raise Exception('A string is required')
        concept = concept.strip()
        if ' ' in concept:
            raise Exception('A single word is required')
        
        #if type(method) not in ()
        
        suggestionsResults = {}
        for met
        
        # There are not any suggestion
        return None
    
    