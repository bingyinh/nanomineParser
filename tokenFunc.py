# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 14:28:55 2021

@author: jafac
"""

def tokenFind(unit):
    
    tokens = []
    newToken = ""
    char = unit
    for i in range(len(unit)):
        if char[0].isalpha() or char[0].isdigit():
            newToken = newToken + char[0]
        else:
            tokens.append(newToken)
            newToken = ""
        char = char[1:]
    tokens.append(newToken)
    return tokens

    
        
print(tokenFind("centimeter/seconds^2"))
        
            