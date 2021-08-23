# nanomineParser
This python module takes in axis labels of scientific plots and returns splited and standardized parameter names/units as part of the NanoMine curation process.

### 1. System preparations

Required packages:

- lxml
  - http://lxml.de/
  - xml etree handling

- numpy
  - https://numpy.org/

- pandas
  - https://pandas.pydata.org/

Python built-in packages: json, re, difflib, glob, csv, os, logging

Open the command or terminal and run
```
pip install -r requirements.txt
```

### 2. How to run

See the README in the data_preparation subdirectory for how to update raw data. Once the preparation works are done, in your code, do
```
from spectraHeaderParserForXML import spectraHeaderParserForXML
# default use, pass in the path to the schema file
shpxml = spectraHeaderParserForXML(xsdDir)
# if you place nanomineParserConfig.json in another directory, you 
# will need to pass that into the argument of spectraHeaderParserForXML
shpxml = spectraHeaderParserForXML(xsdDir, 'your_new_path_to_json')
```
Use runOnXML to update xml, identify if you would like to overwrite or create a copy of the xml file indicated by the `xmlName` parameter
```
shpxml.runOnXML(xmlName, createCopy=False) # overwrite
shpxml.runOnXML(xmlName, createCopy=True) # create a copy
```
