import pandas as pd
import json

# read the polished Excel file of raw data
df = pd.read_excel('rawDataUnique.xlsx',index_col=None,keep_default_na=False)

# initialize dicts
stdXNameXName = {}
stdYNameYName = {}
stdXUnitXUnit = {}
stdYUnitYUnit = {}
xUnitTypeStdXUnit = {}
yUnitTypeStdYUnit = {}
stdXNameXUnitType = {}
stdYNameYUnitType = {}
xRawXNameXUnit = {} # only for spliting fn training purpose
yRawYNameYUnit = {} # only for spliting fn training purpose
xPathStdXName = {}
xPathStdYName = {}

for row in df.iterrows():
    rowData = row[1] # row[0] is the index, row[1] is the series
    # if stdXName exists
    if rowData['stdXName']:
        if rowData['xName']:
            # build stdXName-xName
            if rowData['stdXName'] not in stdXNameXName:
                stdXNameXName[rowData['stdXName']] = set()
            stdXNameXName[rowData['stdXName']].add(rowData['xName'])
            # build xRaw_header-(xName,xUnit)
            if rowData['xRaw_header'] not in xRawXNameXUnit:
                xRawXNameXUnit[rowData['xRaw_header']] = set()
            xRawXNameXUnit[rowData['xRaw_header']].add((rowData['xName'],
                                                        rowData['xUnit']))
        # build xpath-stdXName
        if not rowData['ignore']:
            xpath = rowData['xPath'].replace('/data','').replace('/Data','')
            if xpath not in xPathStdXName:
                xPathStdXName[xpath] = set()
            xPathStdXName[xpath].add(rowData['stdXName'])
    # if stdXUnit exists
    if rowData['stdXUnit']:
        # build stdXUnit-xUnit
        if rowData['stdXUnit'] not in stdXUnitXUnit:
            stdXUnitXUnit[rowData['stdXUnit']] = set()
        stdXUnitXUnit[rowData['stdXUnit']].add(rowData['xUnit'])
        # build xUnitType-stdXUnit
        if rowData['xUnitType']:
            if rowData['xUnitType'] not in xUnitTypeStdXUnit:
                xUnitTypeStdXUnit[rowData['xUnitType']] = set()
            xUnitTypeStdXUnit[rowData['xUnitType']].add(rowData['stdXUnit'])
    # if both stdXName and xUnitType exist
    if rowData['stdXName'] and rowData['xUnitType']:
        # build stdXName-xUnitType
        if rowData['stdXName'] not in stdXNameXUnitType:
            stdXNameXUnitType[rowData['stdXName']] = set()
        stdXNameXUnitType[rowData['stdXName']].add(rowData['xUnitType'])
    # if stdYName eyists
    if rowData['stdYName']:
        if rowData['yName']:
            # build stdYName-yName
            if rowData['stdYName'] not in stdYNameYName:
                stdYNameYName[rowData['stdYName']] = set()
            stdYNameYName[rowData['stdYName']].add(rowData['yName'])
            # build yRaw_header-(yName,yUnit)
            if rowData['yRaw_header'] not in yRawYNameYUnit:
                yRawYNameYUnit[rowData['yRaw_header']] = set()
            yRawYNameYUnit[rowData['yRaw_header']].add((rowData['yName'],
                                                        rowData['yUnit']))
        # build xpath-stdYName
        if not rowData['ignore']:
            xpath = rowData['xPath'].replace('/data','').replace('/Data','')
            if xpath not in xPathStdYName:
                xPathStdYName[xpath] = set()
            xPathStdYName[xpath].add(rowData['stdYName'])
    # if stdYUnit eyists
    if rowData['stdYUnit']:
        # build stdYUnit-yUnit
        if rowData['stdYUnit'] not in stdYUnitYUnit:
            stdYUnitYUnit[rowData['stdYUnit']] = set()
        stdYUnitYUnit[rowData['stdYUnit']].add(rowData['yUnit'])
        # build yUnitType-stdYUnit
        if rowData['yUnitType']:
            if rowData['yUnitType'] not in yUnitTypeStdYUnit:
                yUnitTypeStdYUnit[rowData['yUnitType']] = set()
            yUnitTypeStdYUnit[rowData['yUnitType']].add(rowData['stdYUnit'])
    # if both stdYName and yUnitType eyist
    if rowData['stdYName'] and rowData['yUnitType']:
        # build stdYName-yUnitType
        if rowData['stdYName'] not in stdYNameYUnitType:
            stdYNameYUnitType[rowData['stdYName']] = set()
        stdYNameYUnitType[rowData['stdYName']].add(rowData['yUnitType'])


# dump all these dict into a json file
fullDict = {'stdXName-xName':stdXNameXName,
            'stdYName-yName':stdYNameYName,
            'stdXUnit-xUnit':stdXUnitXUnit,
            'stdYUnit-yUnit':stdYUnitYUnit,
            'xUnitType-stdXUnit':xUnitTypeStdXUnit,
            'yUnitType-stdYUnit':yUnitTypeStdYUnit,
            'stdXName-xUnitType':stdXNameXUnitType,
            'stdYName-yUnitType':stdYNameYUnitType,
            'xRaw-xName-xUnit':xRawXNameXUnit,
            'yRaw-yName-yUnit':yRawYNameYUnit,
            'xPath-stdXName':xPathStdXName,
            'xPath-stdYName':xPathStdYName}
# prepare for json serialization, convert set into list
for pairDict in fullDict:
    for pair in fullDict[pairDict]:
        fullDict[pairDict][pair] = list(fullDict[pairDict][pair])

with open('nanomineParserConfig.json','w') as f:
    json.dump(fullDict,f)