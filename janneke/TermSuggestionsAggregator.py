#!/usr/bin/env python
################################################################################
#    Created by Oscar Martinez                                                 #
#    o.rubi@esciencecenter.nl                                                  #
################################################################################

class Aggregation:
    Average, Sum = range(2)

class TermSuggestionsAggregator:
    """Class used to combine/aggregate term suggestions from different methods."""
    def getSuggestions(self, term, methods, aggregation=Aggregation.Average):
        """Get suggestions to a term."""
        # Check that term is a string and a single word
        if type(term) != str:
            raise Exception('A string is required')
        term = term.strip()
        if ' ' in term:
            raise Exception('A single word is required')
        
        # Get the suggestion set from each method
        methodsSuggestions = []
        for method in methods:
            ts = method.suggest_terms(term)
            if len(ts):
                # We need to normalize the weights of the terms (0,1)
                maxWeight = max(ts.values())
                for t in ts:
                    ts[t] = ts[t] / maxWeight
                methodsSuggestions.append(ts)

        # Each method returns a suggestion set which is dictionary in the form of:
        # {str : float, str : float, ...} where str is a suggested term and float is the weight of the suggestion (how relevant it is)
        
        # We compile a final suggestion set which is the combination of the suggestions set from the various methods
        
        # There are several methods to do this
        finalSuggestions = {}
        if aggregation == Aggregation.Average:
            # The weight is the final suggestion set is the average of weights in the other sets
            for methodSuggestions in methodsSuggestions:
                if methodSuggestions is not None:
                    for s in methodSuggestions:
                        if s in finalSuggestions:
                            finalSuggestions[s].append(methodSuggestions[s])
                        else:
                            finalSuggestions[s] = [methodSuggestions[s],]
            for s in finalSuggestions:
                finalSuggestions[s] = sum(finalSuggestions[s])/float(len(finalSuggestions[s]))
        elif aggregation == Aggregation.Sum:
            # The weight is the final suggestion set is the sum of weights in the other sets
            for methodSuggestions in methodsSuggestions:
                if methodSuggestions is not None:
                    for s in methodSuggestions:
                        if s in finalSuggestions:
                            finalSuggestions[s] += methodSuggestions[s]
                        else:
                            finalSuggestions[s] = methodSuggestions[s]
        return finalSuggestions