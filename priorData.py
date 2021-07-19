from glob import glob
from lxml import etree
import csv
import re

def separator(xheader, yheader):
    isxhead = True
    for header in [xheader, yheader]:
        
    # ***
    
        rawUnit = "(dimensionless*)"
        rawType = "NA"
        
        head = str(header)
    
        head = head.replace("[", "(")
        head = head.replace("{", "(")
        head = head.replace("]", ")")
        head = head.replace("}", ")")
        
        testUnit = ""
        testType = ""
        trigger = ["ratio", "factor", "normalized"]
        triggered = False
        for i in trigger:
            if i in head:
                testUnit = "(dimensionless)"
                testType = head
                triggered = True
        if not triggered:
            if "(" and ")" in head: # think about how to use inputs from xpath separator to help with the cases when there are multiple parenthesis
                testUnit = head[head.find("(") + 1:head.find(")",-1)]
                testType = head[:head.find("(")]
                if "%" in testUnit:
                    testUnit = "%"
            elif "/" in head:
                testUnit = head[head.find("/") + 1:]
                testType = head[:head.find("/")]
                if "%" in testUnit:
                    testUnit = "%"
            elif "-" in head:
                testUnit = head[head.find("-") + 1:]
                testType = head[:head.find("-")]
                if "%" in testUnit:
                    testUnit = "%"
        testType = testType.strip()

        rawUnit = testUnit
        rawType = testType
        
        # ***
        
        if isxhead:
            xUnit = rawUnit
            xName = rawType
            isxhead = False
        else:
            yUnit = rawUnit
            yName = rawType
            
    return (xName.lower(), xUnit.lower().replace(" ",""), 
            yName.lower(), yUnit.lower().replace(" ",""))

def simpDict():
    pastUnits = {}
    pastTypes = {}
            
    # Find unique simplified values from all identical xpaths
    with open('typePath.csv', encoding='utf-8-sig', mode='r') as csv_unit:
        csv_reader = csv.reader(csv_unit)
        for row in csv_reader:
            pastUnits[row[0].lower()] = row[2].lower()
                
    with open('unitPath.csv', encoding='utf-8-sig', mode='r') as csv_unit:
        csv_reader = csv.reader(csv_unit)
        for row in csv_reader:
            pastTypes[row[1].lower().replace(" ","")] = row[0].lower().replace(" ","")
                    
    return [pastUnits, pastTypes]

# initialize a data structure to save all extracted information
xmlData = []
# create a list of path to xml files using glob
xmls = glob('/Users/jafac/xmlALL/xmlFULL**/*.xml', 
                   recursive = True)
# create list to identify partial xml files
emptyList = []
# create list to identify all units
listUnit = []
listPaths = []


for xml in xmls:
    try:
        # load xml with lxml.etree
        tree = etree.parse(xml)
        # find all headers in the xml and their element path
        dictionary = simpDict()
        for node in tree.findall('.//data[data]'):
            xpath = tree.getelementpath(node) # might have index in the element path
            # extract data/data/headers/column
            headers = node.find('.//headers')
            xAxis = headers[0].text
            yAxis = headers[1].text
            # find all generated xName, xUnit, yName, yUnit in AxisLabel
            axisLabel = node.find('AxisLabel')
            
            xpath = re.sub(r'\[.*?\]','',xpath)
            if '/data/data' in xpath:
                xpath = xpath[:xpath.rfind('/data')]
            xpath = xpath[:xpath.rfind('/data')]
            
            rawData = separator(xAxis, yAxis)
            
            cleanxname = ""
            cleanxunit = ""
            cleanyname = ""
            cleanyunit = ""
            
            # dict 0 is types, dict 1 is units
            # rawdata 0: xname, 1: 
            
            if rawData[0] in dictionary[0].values() or rawData[0] in dictionary[0].keys():
                cleanxname = dictionary[0][rawData[0]]
                
            if rawData[1] in dictionary[1].values() or rawData[1] in dictionary[1].keys():
                cleanxunit = dictionary[1][rawData[1]]
           
            if rawData[2] in dictionary[0].values() or rawData[2] in dictionary[0].keys():
                cleanyname = dictionary[0][rawData[2]]
            
            if rawData[3] in dictionary[1].values() or rawData[3] in dictionary[1].keys():
                cleanyunit = dictionary[1][rawData[3]]

            # save to the data structure
            xmlData.append((xpath, rawData[0], cleanxname, rawData[1], cleanxunit, 
                            rawData[2], cleanyname, rawData[3], cleanyunit))
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    
with open('priorData.csv','w+',encoding='utf-8',newline='') as f:
    print("writing csv")
    writer = csv.writer(f)
    writer.writerow(['xpath','xNameRaw','xNameClean', 'xUnitRaw','xUnitClean',
                     'yNameRaw','yNameClean','yUnitRaw','yUnitClean'])
    for row in xmlData:
        writer.writerow(row)