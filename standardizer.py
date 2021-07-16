import numpy
# A parent standardizer object
class standardizer(object):
    def __init__(self, namePairs):
        '''
        Initialize and set up name pairs of non-standard and standard expressions

        :param namePairs: a dictionary with standard expressions as the key and a set of non-standard expressions as the value. Example: {'Storage Modulus': {"E'", "Storage Modulus", "Log-storage modulus", "Storage Modulus, E"}} or {'Hz': {'Hertz', 'Hz'}, 'kHz': {'kHz'}, 'GHz': {'GHz'}, 'rad/second': {'rad/s', 'rad/sec'}}
        :type namePairs: dict
        '''
        self.namePairs = namePairs

    def evaluate(self, expression):
        '''
        Calls mapping algorithms to evaluate if a match in the standard expressions could be found for the given expression

        :param expression: could be raw xName, xUnit, yName, yUnit
        :type expression: str

        :returns: standard expression (or None if no match could be found)
        :rtype: str
        '''
        # call algorithm 1 (e.g. matchFunc, you might want to ignore cases)
        raw = expression.lower().replace(" ","")
        for stdName in self.namePairs: 
            if raw == stdName.lower().replace(" ",""):
                return stdName
            for rawName in self.namePairs[stdName]:
                if raw == rawName.lower().replace(" ",""):
                    return stdName
            

        #***

        # call algorithm 2 (e.g. levenshtein distance with a threshold)
        distanceLow = []
        token1 = expression
        for stdName in self.namePairs: 
            for token2 in self.namePairs[stdName]:
                if len(token2) > 3:
            #***
                    distances = numpy.zeros((len(token1) + 1, len(token2) + 1))
                
                    for t1 in range(len(token1) + 1):
                        distances[t1][0] = t1
                
                    for t2 in range(len(token2) + 1):
                        distances[0][t2] = t2
                        
                    a = 0
                    b = 0
                    c = 0
                    
                    for t1 in range(1, len(token1) + 1):
                        for t2 in range(1, len(token2) + 1):
                            if (token1[t1-1] == token2[t2-1]):
                                distances[t1][t2] = distances[t1 - 1][t2 - 1]
                            else:
                                a = distances[t1][t2 - 1]
                                b = distances[t1 - 1][t2]
                                c = distances[t1 - 1][t2 - 1]
                                
                                if (a <= b and a <= c):
                                    distances[t1][t2] = a + 1
                                elif (b <= a and b <= c):
                                    distances[t1][t2] = b + 1
                                else:
                                    distances[t1][t2] = c + 1
                
                    if distances[len(token1)][len(token2)] < 1:
                        distanceLow.append(token2)
        #***
       
        for token2 in self.namePairs:
            if len(token2) > 3:
        #***
                distances = numpy.zeros((len(token1) + 1, len(token2) + 1))
            
                for t1 in range(len(token1) + 1):
                    distances[t1][0] = t1
            
                for t2 in range(len(token2) + 1):
                    distances[0][t2] = t2
                    
                a = 0
                b = 0
                c = 0
                
                for t1 in range(1, len(token1) + 1):
                    for t2 in range(1, len(token2) + 1):
                        if (token1[t1-1] == token2[t2-1]):
                            distances[t1][t2] = distances[t1 - 1][t2 - 1]
                        else:
                            a = distances[t1][t2 - 1]
                            b = distances[t1 - 1][t2]
                            c = distances[t1 - 1][t2 - 1]
                            
                            if (a <= b and a <= c):
                                distances[t1][t2] = a + 1
                            elif (b <= a and b <= c):
                                distances[t1][t2] = b + 1
                            else:
                                distances[t1][t2] = c + 1
            
                if distances[len(token1)][len(token2)] < 2:
                    distanceLow.append(token2)
        #*** 
        
        # call algorithm 3 (e.g. tokenization)

        # etc.
        
        # summarize the results from the evaluations of all algorithms, think about some rules that could conclude whether a match could be found, return the match
            # Match: if match, return key
            # Distance: stated above
            # Token: if tokens are the same and distance is < 3 or something like that
        if len(distanceLow) == 1:
            return self.namePairs[distanceLow[0]]
        # otherwise, return None
        return None
