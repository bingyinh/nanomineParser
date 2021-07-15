import csv
import numpy

# Put reference here
# can be used as autocorrect
# rules: can be 2 away from normalized, 1 away from variant 
# if more than 1 possible outcomes, returns list of them

def levenshteinDistanceDP(token1, token2):
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
    return distances[len(token1)][len(token2)]

# read in name, stdName pairs
namePairs = {} # {stdName: set(name)}
with open('simplifyUnits.csv', encoding='utf-8-sig', mode='r') as csv_unit:
    csv_reader = csv.reader(csv_unit)
    for row in csv_reader:
        key = row[0]
        values = set(row[1:])
        if key not in namePairs:
            namePairs[key] = set()
        namePairs[key].update(values)

distancesPairs = {} # {deg C: {Gpa: some score, celsius: some score, ...}}
correctPairs = [] # to store scores of every correct pairs
wrongPairs = []

for key in namePairs:
    names = namePairs[key]
    for name in names:
        if name not in distancesPairs:
            distancesPairs[name] = {}
        for stdName in namePairs.keys():
            score = levenshteinDistanceDP(name, stdName)
            distancesPairs[name][stdName] = score
            if key == stdName:
                correctPairs.append(score)
            else:
                wrongPairs.append(score)

def cutoffAcc(correctPairs, wrongPairs, thresh):
    totalNumPairs = len(correctPairs) + len(wrongPairs)
    posConsideredPos = 0
    posConsideredNeg = 0
    negConsideredPos = 0
    negConsideredNeg = 0
    totalPos = len(correctPairs)
    totalNeg = len(wrongPairs)
    for i in correctPairs:
        if i <= thresh:
            posConsideredPos += 1
        else:
            posConsideredNeg += 1
    for i in wrongPairs:
        if i <= thresh:
            negConsideredPos += 1
        else:
            negConsideredNeg += 1
    return (posConsideredPos, posConsideredNeg, negConsideredPos, negConsideredNeg)

worstPairScore = 15
print("             (TP, FN, FP, TN")
for thresh in range(worstPairScore):
    print("Thresh is {}".format(thresh),cutoffAcc(correctPairs, wrongPairs, thresh))

