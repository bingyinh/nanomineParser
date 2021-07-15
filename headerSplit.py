from glob import glob
from lxml import etree
import csv

# function to add units to master list
def addUnit(unit):
    with open('unitCSVMaster.csv','a',encoding='utf-8-sig',newline='') as f:
        print ("adding unit: " + str(unit))
        writer = csv.writer(f)
        writer.writerow([str(unit).lower()])

# populate unitList with known units
def unitFind():
    unitList = [] 
    with open('unitCSVMaster.csv', encoding='utf-8-sig', mode='r') as csv_unit:
        csv_reader = csv.DictReader(csv_unit)
        for row in csv_reader:
            unitList.append(row["Units"].lower()) # I think there's an error here right now
    return unitList

# populate headerList with headers
def headerFind():
    
    headerList = []
    emptyList = []
    # create a list of path to xml files using glob
    xmls = glob('/Users/jafac/xmlALL/xmlFULL**/*.xml', 
                   recursive = True)
    # loop through each xml file
    for xml in xmls:
        # load xml with lxml.etree
        try:
            tree = etree.parse(xml)
            # find all headers in the xml and their element path
            for node in tree.findall('.//data[data]'):
                path = str(tree.getelementpath(node)) # might have index in the element path
                while (str(path).count("[")):
                    path = path[:path.index("[")] + path[path.index("]") + 1:]
                # extract data/data/headers/column
                headers = node.find('.//headers')
                if headers[0].text:
                    xAxis = headers[0].text
                    headerList.append([xAxis, path, xml])
                if headers[1].text:
                    yAxis = headers[1].text
                    headerList.append([yAxis, path, xml])
        except:
            emptyList.append([xml])
    # print (emptyList)
    return headerList
        
# separate unit and name within header
def findUnit(header, unitList):
    
    name = header
    realUnit = "(dimensionless)"
    confidence = 0
    
# check for dimensionless trigger word
    trigger = ["ratio", "factor", "normalized", "%"] 
    for i in trigger:
        if i in name:
            confidence += 1
            return [realUnit, name, confidence]     
        
# check for brackets
    head = header
    
    head = head.replace("[", "(")
    head = head.replace("{", "(")
    head = head.replace("]", ")")
    head = head.replace("}", ")")
    
    if "(" and ")" in head:
        name = head[:head.find("(") - 1]
        
        unit = head[head.find("("):].lower().replace(" ","")
        
        while unit.count("("):
            
            beg = unit.find("(", 0) + 1
            end = unit.find(")", -1)
            
            unit = unit[beg:end]
            
            for i in unitList:
                if unit == i.lower().replace(" ",""):
                    confidence += 1
                    return [unit, name, confidence]

    return [realUnit, name, confidence]
              
#  
def simplify(oldUnit, unitDict):
    try:
        return unitDict[oldUnit]
    except:
        print(str(oldUnit) + " not in dict")     

# initialize a data structure to save all extracted information
xmlData = []

headerInfo = headerFind()
headers = [h[0] for h in headerInfo]
unitList = unitFind()

masterList = []
simplifiedUnits = {}

with open('simplifyUnits.csv', encoding='utf-8-sig', mode='r') as csv_unit:
    csv_reader = csv.reader(csv_unit)
    for row in csv_reader:
        value = row[0].lower().replace(" ","")
        for i in row[1:]:        
            simplifiedUnits[i.lower().replace(" ","")] = value

for i in headerInfo:
    try:
        sep = findUnit(i[0], unitList)
        
        sim = simplify(sep[0], simplifiedUnits)
        
        masterList.append([sep[0], sim, sep[1], i[0], sep[2], i[1], i[2]])
    except:
        xmlData.append(i)
        
with open('parserData.csv','w+',encoding='utf-8-sig',newline='') as f:
    print ("writing csv")
    writer = csv.writer(f)
    writer.writerow(["Units", "Simplified", "Name", "Header", "Confidence", "Path", "File"]) # Do I need this? I don't know yet
    for r in masterList:
        writer.writerow(r)

