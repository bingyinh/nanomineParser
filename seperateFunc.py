import csv

# returns raw type and raw unit, does not require dict

def separate(header):
        rawUnit = "(dimensionless*)"
        rawType = "NA"
        
        head = str(header)
    
        head = head.replace("[", "(")
        head = head.replace("{", "(")
        head = head.replace("]", ")")
        head = head.replace("}", ")")
        
        testUnit = ""
        testType = ""
        trigger = ["ratio", "factor", "normalized", "%"] 
        triggered = False
        for i in trigger:
            if i in head:
                testUnit = "(dimensionless)"
                testType = head
                triggered = True
        if not triggered:
            if "(" and ")" in head:
                testUnit = head[head.find("(") + 1:head.find(")",-1)]
                testUnit = testUnit.lower().replace(" ","")
                testType = head[:head.find("(")]
            elif "/" in head:
                testUnit = head[head.find("/") + 1:]
                testType = head[:head.find("/")]
            elif "-" in head:
                testUnit = head[head.find("-") + 1:]
                testType = head[:head.find("-")]
        
        try:
            if testType[-1] == " ":
                testType = testType[:-1]
        except:
            testType = testType
                
        rawUnit = testUnit
        rawType = testType
        
        return [rawUnit, rawType]
    
dataSet = []
        
with open('comparison.csv', encoding='utf-8-sig', mode='r') as csv_unit:
    csv_reader = csv.reader(csv_unit)
    for row in csv_reader:    
        dataSet.append(separate(row[1]))
        
with open('seperatorTest.csv','w+',encoding='utf-8-sig',newline='') as f:
    print ("writing csv")
    writer = csv.writer(f)
    for r in dataSet:
        writer.writerow(r)
                