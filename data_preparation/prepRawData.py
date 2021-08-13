from glob import glob
from lxml import etree
import csv
import re
import os
import logging

# config logging
logging.basicConfig(filename='prepRawData.log',
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            level = logging.INFO
                           )

# the directory containing all xml files
xmlDir = "D:/Dropbox/DIBBS/nmdata/5e96dbe7c49dc53363c20305"
ignore = {'L194_S1_Maillard_2012.xml'}
# initialize a data structure to save all extracted information
xmlData = []

# create a list of path to xml files using glob
xmls = glob("{}/*.xml".format(xmlDir))
errors = ''

# read nameXpathPairsManualStd.csv
manualStd = {}
with open('nameXpathPairsManualStd.csv','r+',encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['Name'].strip()
        if len(name) == 0:
            continue
        xPath = row['Xpath'].strip()
        stdName = row['StdName'].strip()
        manualStd[(name,xPath)] = stdName

# axisStd fn from XMLCONV
# a helper method to standardize the axis label and axis unit from headers
# handle left for further development (!!!!!!!!) input header is a string
def axisStd(header):
    header = header.strip()
    # replace synonyms
    # breakdown labels and units
        # scan for () [] , /
    puncs = {'(':-1, '[':-1, ',':-1, '/':-1} # init -1 indicates doesn't exist
    for punc in puncs:
        puncs[punc] = header.find(punc)
        if header.find(punc) == -1:
            puncs[punc] = len(header)
        # find the punctuation that appears first
    firstPunc = sorted(puncs, key = puncs.get)[0]
        # if none of the puncs appears, then we have a label and a unit (dimensionless)
    # special case, end with '%' (e.g. strain)
    if header[-1] != '%':
        if puncs[firstPunc] == len(header):
            return (header, 'dimensionless')
        label = header[0:puncs[firstPunc]].strip()
        unit = header[puncs[firstPunc]+1:].strip()
    elif ' ' in header: # unit separated by white space
        label = header[:header.rfind(' ')].strip()
        unit = header[header.rfind(' ')+1:].strip()
    else: # % unit not separated by white space
        label = header[:-1]
        unit = header[-1]
    # standardize label
        # make every leading letter in the label capital
    if len(label) == 1:
        label = label.upper()
    else:
        # if starts with uppercase letters, example: CNF content(phr)
        if label.split(' ')[0].isupper() and len(label.split(' ')) > 1:
            label = label.split(' ')[0] + label[label.find(' '):].lower()
        else:
            label = label[0].upper() + label[1:].lower()
        # other standardize

    # standardize unit
        # remove the other half punctuation if it exists
    if firstPunc == '(':
        unit = unit.strip(')')
    elif firstPunc == '[':
        unit = unit.strip(']')
        # other standardize
    if len(unit) == 0:
        unit = 'dimensionless'

    return (label, unit)

# loop through each xml file
for xml in xmls:
    nextIter = False
    for fn in ignore:
        if fn in xml:
            nextIter = True
    if nextIter:
        continue
    try:
        # split filename
        filename = os.path.split(xml)[-1]
        # load xml with lxml.etree
        tree = etree.parse(xml)
        # find all headers in the xml and their element path
        spectraNodes = []
        spectraParentTags = ['data', 'LoadingProfile', 'MasterCurve', 'profile']
        for tag in spectraParentTags:
            spectraNodes += tree.findall('.//{}[data]'.format(tag))
        for node in spectraNodes:
            xpath = tree.getelementpath(node) # might have index in the element path
            xpath = re.sub(r'\[.*?\]','',xpath)# remove index
            # extract data/data/headers/column
            headers = node.find('.//headers')
            xAxis = headers[0].text
            yAxis = headers[1].text
            # find all generated xName, xUnit, yName, yUnit in AxisLabel
            axisLabel = node.find('AxisLabel')
            xName = None
            xUnit = None
            yName = None
            yUnit = None
            stdXName = None
            stdYName = None
            if axisLabel is None:
                xName, xUnit = axisStd(xAxis)
                yName, yUnit = axisStd(yAxis)
            else:
                xName = axisLabel.findtext('xName')
                xUnit = axisLabel.findtext('xUnit')
                yName = axisLabel.findtext('yName')
                yUnit = axisLabel.findtext('yUnit')
            # see if manual stdName exists
            if (xName, xpath.strip('/data').lower()) in manualStd:
                stdXName = manualStd[(xName, xpath.strip('/data').lower())]
            if (yName, xpath.strip('/data').lower()) in manualStd:
                stdYName = manualStd[(yName, xpath.strip('/data').lower())]

            # save to the data structure
            xmlData.append({'file': filename,
                            'xPath': xpath,
                            'xRaw_header': xAxis,
                            'yRaw_header': yAxis,
                            'xName': xName,
                            'xUnit': xUnit,
                            'yName': yName,
                            'yUnit': yUnit,
                            'stdXName': stdXName,
                            'stdYName': stdYName
                            })
    except Exception as e:
        logging.error(xml, exc_info=e)

# write to a spreadsheet or any other data format of your choice
with open('rawData.csv','w+',encoding='utf-8-sig',newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['file','xPath','xRaw_header',
                                           'yRaw_header','xName','stdXName',
                                           'xUnit','yName','stdYName','yUnit'])
    writer.writeheader()
    for row in xmlData:
        writer.writerow(row)
    print("Done exporting to rawData.csv")

# write to a spreadsheet or any other data format of your choice
with open('xName.csv','w+',encoding='utf-8-sig',newline='') as f:
    writer = csv.DictWriter(f,fieldnames=['file','xPath','xRaw_header','xName',
                                          'stdXName'])
    writer.writeheader()
    for row in xmlData:
        writer.writerow({'file':row['file'],
                         'xPath':row['xPath'],
                         'xRaw_header':row['xRaw_header'],
                         'xName':row['xName'],
                         'stdXName':row['stdXName']})
    print("Done exporting to xName.csv")

# write to a spreadsheet or any other data format of your choice
with open('xUnit.csv','w+',encoding='utf-8-sig',newline='') as f:
    writer = csv.DictWriter(f,fieldnames=['file','xPath','xRaw_header','xUnit'])
    writer.writeheader()
    for row in xmlData:
        writer.writerow({'file':row['file'],
                         'xPath':row['xPath'],
                         'xRaw_header':row['xRaw_header'],
                         'xUnit':row['xUnit']})
    print("Done exporting to xUnit.csv")

# write to a spreadsheet or any other data format of your choice
with open('yName.csv','w+',encoding='utf-8-sig',newline='') as f:
    writer = csv.DictWriter(f,fieldnames=['file','xPath','yRaw_header','yName',
                                          'stdYName'])
    writer.writeheader()
    for row in xmlData:
        writer.writerow({'file':row['file'],
                         'xPath':row['xPath'],
                         'yRaw_header':row['yRaw_header'],
                         'yName':row['yName'],
                         'stdYName':row['stdYName']})
    print("Done exporting to yName.csv")

# write to a spreadsheet or any other data format of your choice
with open('yUnit.csv','w+',encoding='utf-8-sig',newline='') as f:
    writer = csv.DictWriter(f,fieldnames=['file','xPath','yRaw_header','yUnit'])
    writer.writeheader()
    for row in xmlData:
        writer.writerow({'file':row['file'],
                         'xPath':row['xPath'],
                         'yRaw_header':row['yRaw_header'],
                         'yUnit':row['yUnit']})
    print("Done exporting to yUnit.csv")

# export unique rows of rawData into a separate file
xmlDataUnique = []
xmlDataPool = {}
for row in xmlData:
    if (row['xPath'],row['xRaw_header'],row['yRaw_header'],row['xName'],row['stdXName'],row['xUnit'],row['yName'],row['stdYName'],row['yUnit']) not in xmlDataPool:
        xmlDataUnique.append(row)
        xmlDataPool[(row['xPath'],row['xRaw_header'],row['yRaw_header'],row['xName'],row['stdXName'],row['xUnit'],row['yName'],row['stdYName'],row['yUnit'])] = 0
    xmlDataPool[(row['xPath'],row['xRaw_header'],row['yRaw_header'],row['xName'],row['stdXName'],row['xUnit'],row['yName'],row['stdYName'],row['yUnit'])] += 1

with open('rawDataUnique.csv','w+',encoding='utf-8-sig',newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['file','xPath','occurrence',
                                           'xRaw_header','xName','stdXName','xUnit',
                                           'yRaw_header','yName','stdYName','yUnit'])
    writer.writeheader()
    for row in xmlDataUnique:
        row['occurrence'] = xmlDataPool[(row['xPath'],row['xRaw_header'],row['yRaw_header'],row['xName'],row['stdXName'],row['xUnit'],row['yName'],row['stdYName'],row['yUnit'])]
        writer.writerow(row)
    print("Done exporting to rawDataUnique.csv")