#!/usr/bin/env python
################################################################################
#    Created by Oscar Martinez                                                 #
#    o.rubi@esciencecenter.nl                                                  #
################################################################################

class SearchMethodAggregation:
    AverageMethod, SumMethod = range(2)

class TermSuggester:
    """Class used to get suggestions from a term.
    This class is based on using various methods to determine suggestion terms.
    The results from the different methods are in the end combined"""
    def __init__(self, searchMethodClasses, initializeParameters):
        """ Initializes the TermSuggester, i.e. create instances of the modules that are used to get term suggestions. 
        the searchMethodClasses contains the list of classes which instances will be created and used
        initalizeParameters is a list which contains the initialization parameters to be used when creating the different instances"""
        self.searchMethodInstances = []
        
        # Initialize the several searchMethodInstances.
        print 'Creating searchMethod instances: '
        for i in range(len(searchMethodClasses)):
            name = str(i) + '_' + searchMethodClasses[i].__name__
            print '    Name: ' + name
            print '    Class: ' + searchMethodClasses[i].__name__
            print '    InitParams: ' + str(initializeParameters[i])
            print 
            self.searchMethodInstances.append(searchMethodClasses[i](*initializeParameters[i]))
    
    def getSuggestions(self, term, searchMethodAggregation=SearchMethodAggregation.AverageMethod, searchMethodIndexes = None):
        """Get suggestions to a term."""
        # Check that term is a string and a single word
        if type(term) != str:
            raise Exception('A string is required')
        term = term.strip()
        if ' ' in term:
            raise Exception('A single word is required')
        
        if searchMethodIndexes == None:
            searchMethodIndexes = range(len(self.searchMethodInstances))
        
        # Get the suggestion set from each method
        suggestionsResults = []
        for i in searchMethodIndexes:
            ts = self.searchMethodInstances[i].suggest_terms(term)
            if len(ts):
                # We need to normalize the weights of the terms (0,1)
                maxWeight = max(ts.values())
                for t in ts:
                    ts[t] = ts[t] / maxWeight
                suggestionsResults.append(ts)

        # Each method returns a suggestion set which is dictionary in the form of:
        # {str : float, str : float, ...} where str is a suggested term and float is the weight of the suggestion (how relevant it is)
        
        # We compile a final suggestion set which is the combination of the suggestions set from the various methods
        
        # There are several methods to do this
        finalSuggestions = {}
        if searchMethodAggregation == SearchMethodAggregation.AverageMethod:
            # The weight is the final suggestion set is the average of weights in the other sets
            for i in range(len(suggestionsResults)):
                srs = suggestionsResults[i]
                if srs is not None:
                    for s in srs:
                        if s in finalSuggestions:
                            finalSuggestions[s].append(srs[s])
                        else:
                            finalSuggestions[s] = [srs[s],]
            for s in finalSuggestions:
                finalSuggestions[s] = sum(finalSuggestions[s])/float(len(finalSuggestions[s]))
        elif searchMethodAggregation == SearchMethodAggregation.SumMethod:
            # The weight is the final suggestion set is the sum of weights in the other sets
            for i in range(len(suggestionsResults)):
                srs = suggestionsResults[i]
                if srs is not None:
                    for s in srs:
                        if s in finalSuggestions:
                            finalSuggestions[s] += srs[s]
                        else:
                            finalSuggestions[s] = srs[s]
        return finalSuggestions