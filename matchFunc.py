# simple dictionary matching function

def termDict(raw, dictionary):
    if raw in dictionary:
        return dictionary[raw]
    return None