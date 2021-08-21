# test codes for spectraHeaderParser
from spectraHeaderParser import spectraHeaderParser
import pandas as pd
from glob import glob

# create the object
shp = spectraHeaderParser()

## some easy test cases
# test case 1
xpath = 'PROPERTIES/Viscoelastic/DynamicProperties/DynamicPropertyProfile/data'
xheader = 'temperature (deg C)'
yheader = 'storage modulus (Mpa)'
answer = {
    'xName':'Temperature',
    'xUnit':'Celsius',
    'yName':'Storage Modulus',
    'yUnit':'MPa'
}
print(shp.parse(xpath, xheader, yheader))
assert shp.parse(xpath, xheader, yheader) == answer, 'Fail test case 1'
# test case 2
xpath = 'PROPERTIES/Viscoelastic/DynamicProperties/DynamicPropertyProfile'
xheader = 'f (hz)'
yheader = 'tan d (dimensionless)'
answer = {
    'xName':'Frequency',
    'xUnit':'Hz',
    'yName':'Tan Delta',
    'yUnit':'a.u.'
}
print(shp.parse(xpath, xheader, yheader))
assert shp.parse(xpath, xheader, yheader) == answer, 'Fail test case 2'

## batch tests on mapping function
# test using all Excel files in the data_preparation directory
xlsxs = glob('./data_preparation/*.xlsx')
for xlsx in xlsxs:
    df = pd.read_excel(xlsx, index_col=None,
        keep_default_na=False, dtype=str)
    # skip Excel files with wrong header row
    if ('xPath' not in df.columns or 'xRaw_header' not in df.columns or
        'stdXName' not in df.columns or 'stdXUnit' not in df.columns or
        'yRaw_header' not in df.columns or 'ignore' not in df.columns or
        'stdYName' not in df.columns or 'stdYUnit' not in df.columns):
        continue
    print("Testing using {}".format(xlsx))
    # read Excel and test by row
    for row in df.iterrows():
        rowData = row[1] # row[0] is the index, row[1] is the series
        # skip rows that are ignored or have empty values for stdX/YName/Unit or
        # xName or yName (note that xUnit and yUnit could be empty)
        if (rowData['ignore'] or (not rowData['xRaw_header']) or
            (not rowData['stdXName']) or (not rowData['stdXUnit']) or
            (not rowData['stdYName']) or (not rowData['stdYUnit']) or
            (not rowData['yRaw_header']) or (not rowData['xName']) or
            (not rowData['yName'])):
            continue
        # test mapping function
        xpath = rowData['xPath']
        xheader = rowData['xRaw_header']
        yheader = rowData['yRaw_header']
        xName = rowData['xName']
        xUnit = rowData['xUnit']
        yName = rowData['yName']
        yUnit = rowData['yUnit']
        answer = {'xName':rowData['stdXName'],
                  'xUnit':rowData['stdXUnit'],
                  'yName':rowData['stdYName'],
                  'yUnit':rowData['stdYUnit']}
        result = shp.mapping(xpath, xName, xUnit, yName, yUnit)
        if result != answer:
            print('''Fail batch test cases {}
Returned: {}
Expected: {}
Raw:
{}'''.format(row[0], result, answer, rowData))

## batch tests on separator

# print("All tests passed")