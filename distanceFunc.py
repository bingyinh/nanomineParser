import csv
        
import numpy
    
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


distanceList = []
altDistanceList = []
with open('simplifyUnits.csv', encoding='utf-8-sig', mode='r') as csv_unit:
    csv_reader = csv.reader(csv_unit)
    for row in csv_reader:
        for i in row[1:]: 
            if len(i) > 3:
                distanceList.append([levenshteinDistanceDP(row[0], i), row[0], i])
                
with open('simplifyUnits.csv', encoding='utf-8-sig', mode='r') as csv_unit:
    csv_reader = csv.reader(csv_unit)        
    rowList = ['']
    for row in csv_reader:
        for i in row:
            if len(i) > 3:
                rowList.append(i)
    altDistanceList.append(rowList)
        
    distanceRow = []
    for i in rowList[1:]:
        distanceRow = [i]
        for j in rowList[1:]:
            distanceRow.append(levenshteinDistanceDP(i, j))
        altDistanceList.append(distanceRow)
            
with open('distanceTest1.csv','w+',encoding='utf-8-sig',newline='') as f:
    print ("writing csv")
    writer = csv.writer(f)
    for r in distanceList:
        writer.writerow(r)
        
with open('distanceTest2.csv','w+',encoding='utf-8-sig',newline='') as f:
    print ("writing csv")
    writer = csv.writer(f)
    for r in altDistanceList:
        writer.writerow(r)
            
            
