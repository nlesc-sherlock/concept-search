#!/usr/bin/env python
################################################################################
#    Created by Oscar Martinez                                                 #
#    o.rubi@esciencecenter.nl                                                  #
################################################################################
import multiprocessing, time

class Aggregation:
    Average, Sum = range(2)

class TermSuggestionsAggregator:
    """Class used to combine/aggregate term suggestions from different methods."""
    
    def runChild(self, childIndex, childrenQueue, resultQueue, term):
        kill_received = False
        while not kill_received:
            job = None
            try:
                # This call will patiently wait until new job is available
                job = childrenQueue.get()
            except:
                # if there is an error we will quit the loop
                kill_received = True
            if job == None:
                # If we receive a None job, it means we can stop the grandchildren too
                kill_received = True
            else:            
                method = job
                ti = time.time()
                try:
                    ts = method.suggest_terms(term)
                    if len(ts):
                        # We need to normalize the weights of the terms (0,1)
                        maxWeight = max(ts.values())
                        for t in ts:
                            ts[t] = ts[t] / maxWeight
                except Exception,e:
                    ts = {}
                    print 'ERROR running ' + method.__class__.__name__ + ':\n' + str(e)
                resultQueue.put([childIndex, method.__class__.__name__, ts, time.time() - ti])
    
    def getSuggestions(self, term, methods, aggregation=Aggregation.Average, numProcesses=1):
        """Get suggestions to a term."""
        # Check that term is a string and a single word
        if type(term) != str:
            raise Exception('A string is required')
        term = term.strip()
        if ' ' in term:
            raise Exception('A single word is required')
        
        childrenQueue = multiprocessing.Queue()
        for method in methods:
            childrenQueue.put(method)
        for i in range(numProcesses): #we add as many None jobs as numProcesses to tell them to terminate (queue is FIFO)
            childrenQueue.put(None)
            
        resultQueue = multiprocessing.Queue() # The queue where to put the results
        children = []
        # We start numProcessesLoad children processes
        for i in range(numProcesses):
            children.append(multiprocessing.Process(target=self.runChild,
                args=(i, childrenQueue, resultQueue, term)))
            children[-1].start()
        
        methodsSuggestions = []
        for i in range(len(methods)):        
                [childIdentifier, methodName, ts, t] = resultQueue.get()
                print 'Child #%d ran %s in %.2f seconds and generated %d term suggestions' % (childIdentifier, methodName, t, len(ts))
                methodsSuggestions.append(ts)
        
        # wait for all children to finish their execution
        for i in range(numProcesses):
            children[i].join()
        

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