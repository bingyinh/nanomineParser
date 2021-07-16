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

        # call algorithm 2 (e.g. levenshtein distance with a threshold)
        
        # etc.
        
        # summarize the results from the evaluations of all algorithms, think about some rules that could conclude whether a match could be found, return the match

        # otherwise, return None
        return None
