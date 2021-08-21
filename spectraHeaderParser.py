# skeleton of the big parser class
import json
from lxml import etree
from standardizer import standardizer
import re

class spectraHeaderParser(object):
    # init function
    def __init__(self):
        # initialize subclasses
        self.__loadSC__()
        pass

    # header separator function (TODO)
    def separator(self, xheader, yheader):
        # replace these with your separator fn!!!!
        xName = xheader[:xheader.find('(')]
        yName = yheader[:yheader.find('(')]
        xUnit = xheader[xheader.find('(')+1:xheader.find(')')]
        yUnit = yheader[yheader.find('(')+1:yheader.find(')')]
        return (xName, xUnit, yName, yUnit)

    # xpath reader function
    def xpathReader(self, xpath):
        '''
        Reads xpath and determines subclasses for xName, xUnit, yName, yUnit individually

        :param xpath: xpath of the spectra data headers
        :type xpath: str

        :returns: a dictionary {'xName': {subclass1, subclass2,...}, 'xUnit': {subclass2}, 'yName': {subclass3}, 'yUnit': {subclass4}}
        :rtype: dict
        '''

        # remove '/data' and '/Data' from xpath, that's a schema thing
        xpath = xpath.replace('/data','').replace('/Data','')
        # remove brackets from xpath
        noBracketXpath = re.sub(r'\[.*?\]','',xpath)
        return self.xpathSubclassPairs[noBracketXpath]

    # preload subclasses
    def __loadSC__(self, config='./data_preparation/nanomineParserConfig.json'):
        '''
        Load standard/non-standard name pairs and load subclasses with those pairs
        '''
        # load json
        with open(config,'r') as f:
            fullDict = json.load(f)
        # load namePairs for stdName and name mapping, X/Y both included
        nameStdzrs = {}
        stdNameName = fullDict['stdName-name']
        for stdName in stdNameName:
            # create the standardizer object and save it to the stdzrs dict
            nameStdzrs[stdName] = standardizer({stdName:stdNameName[stdName]})
        # load namePairs for stdUnit and unit mapping, X/Y both included
        # an extra layer is needed for unit standardizers because one unit type
        # could contain multiple stdUnits
        # example: frequencyUnit: Hz, kHz, MHz, GHz, rad/s
        unitTypeStdzrs = {}
        unitTypeStdUnit = fullDict['unitType-stdUnit']
        stdUnitUnit = fullDict['stdUnit-unit']
        for unitType in unitTypeStdUnit:
            # use unitType as the key, find all stdUnit mapped to the unitType,
            # create a unitType standardizer with all stdUnit-unit pairs
            allStdUnitUnitPairs = {}
            for stdUnit in unitTypeStdUnit[unitType]:
                allStdUnitUnitPairs[stdUnit] = stdUnitUnit[stdUnit]
            # create the standardizer object and save it to the stdzrs dict
            unitTypeStdzrs[unitType] = standardizer(allStdUnitUnitPairs)
        # an example of how xpath-subclass pairs should look like
        # xpathSubclassPairs = {
        #     'PROPERTIES/Viscoelastic/DynamicProperties/DynamicPropertyProfile': {
        #         'xName': {
        #             frequency standardizer object,
        #             temperature standardizer object,
        #             strain standardizer object
        #         },
        #         'xUnit': {
        #             frequencyUnit standardizer object,
        #             temperatureUnit standardizer object,
        #             strainUnit standardizer object,
        #             dimensionless standardizer object
        #         },
        #         'yName': {
        #             storageModulus standardizer object,
        #             lossModulus standardizer object,
        #             tanDelta standardizer object,
        #             normalizedStorageModulus standardizer object,
        #             normalizedLossModulus standardizer object,
        #             normalizedTanDelta standardizer object,
        #             shearStorageModulus standardizer object,
        #             shearLossModulus standardizer object
        #         },
        #         'yUnit': {
        #             modulusUnit standardizer object,
        #             dimensionless standardizer object
        #         }
        #     }
        # }
        xpathSubclassPairs = {}
        stdNameUnitType = fullDict['stdName-unitType']
        xpathStdXName = fullDict['xPath-stdXName']
        xpathStdYName = fullDict['xPath-stdYName']
        # xpathStdXName and xpathStdYName has the same set of keys
        for xpath in xpathStdXName:
            # create the set of standardizers for xName
            xNameStdzrs = set()
            for stdXName in xpathStdXName[xpath]:
                xNameStdzrs.add(nameStdzrs[stdXName])
            # repeat for yName
            yNameStdzrs = set()
            for stdYName in xpathStdYName[xpath]:
                yNameStdzrs.add(nameStdzrs[stdYName])
            # create the set of standardizers for xUnit, this set needs to be
            # created by this route:
            # xpath-stdXName -> stdName-UnitType -> unitTypeStdzrs[xUnitType]
            xUnitStdzrs = set()
            for stdXName in xpathStdXName[xpath]:
                for xUnitType in stdNameUnitType[stdXName]:
                    xUnitStdzrs.add(unitTypeStdzrs[xUnitType])
            # repeat for yUnit
            yUnitStdzrs = set()
            for stdYName in xpathStdYName[xpath]:
                for yUnitType in stdNameUnitType[stdYName]:
                    yUnitStdzrs.add(unitTypeStdzrs[yUnitType])
            # save to xpathSubClassPairs
            xpathSubclassPairs[xpath] = {'xName': xNameStdzrs,
                                         'xUnit': xUnitStdzrs,
                                         'yName': yNameStdzrs,
                                         'yUnit': yUnitStdzrs}
        # save to the class
        self.xpathSubclassPairs = xpathSubclassPairs
        return

    # parse function
    def parse(self, xpath, xheader, yheader):
        '''
        Parses the input raw data and returns the standardized x/yName/Unit

        :param xpath: xpath of the spectra data headers
        :type xpath: str

        :param xheader: raw header string for x axis
        :type xpath: str

        :param yheader: raw header string for y axis
        :type xpath: str

        :returns: a dictionary {'xName': std xName, 'xUnit': std xUnit, 'yName': std yName, 'yUnit': std yUnit (or None as the value if no standard expression could be found)}
        :rtype: dict
        '''
        # separate headers
        xName, xUnit, yName, yUnit = self.separator(xheader, yheader)
        # call mapping function
        return self.mapping(xpath, xName, xUnit, yName, yUnit)

    # mapping function
    def mapping(self, xpath, xName, xUnit, yName, yUnit):
        '''
        Maps xName, xUnit, yName, yUnit with their corresponding std expression.
        Returns the standardized x/yName/Unit

        :param xpath: xpath of the spectra data headers
        :type xpath: str

        :param xName: parameter name for x axis as splitted from raw header str
        :type xName: str

        :param xUnit: unit for x axis as splitted from raw header str
        :type xUnit: str

        :param yName: parameter name for y axis as splitted from raw header str
        :type yName: str

        :param yUnit: unit for y axis as splitted from raw header str
        :type yUnit: str

        :returns: a dictionary {'xName': std xName, 'xUnit': std xUnit, 'yName': std yName, 'yUnit': std yUnit (or None as the value if no standard expression could be found)}
        :rtype: dict
        '''
        # init output
        output = {
            'xName': None,
            'xUnit': None,
            'yName': None,
            'yUnit': None
        }
        # read xpath to determine subclasses
        subclassPools = self.xpathReader(xpath)
        # For cases where multiple paired subclasses, use the one with the
        # highest score
        # standardize xName
        stdXName = None
        stdXNameScore = -1
        for subclass in subclassPools['xName']:
            result, score = subclass.evaluate(xName)
            if score > stdXNameScore:
                stdXName = result
                stdXNameScore = score
        output['xName'] = stdXName
        # standardize xUnit
        # (TODO) use stdX/YName to aid standardizing x/yUnit
        stdXUnit = None
        stdXUnitScore = -1
        for subclass in subclassPools['xUnit']:
            result, score = subclass.evaluate(xUnit)
            if score > stdXUnitScore:
                stdXUnit = result
                stdXUnitScore = score
        output['xUnit'] = stdXUnit
        # standardize yName
        stdYName = None
        stdYNameScore = -1
        for subclass in subclassPools['yName']:
            result, score = subclass.evaluate(yName)
            if score > stdYNameScore:
                stdYName = result
                stdYNameScore = score
        output['yName'] = stdYName
        # standardize yUnit
        # (TODO) use stdX/YName to aid standardizing x/yUnit
        stdYUnit = None
        stdYUnitScore = -1
        for subclass in subclassPools['yUnit']:
            result, score = subclass.evaluate(yUnit)
            if score > stdYUnitScore:
                stdYUnit = result
                stdYUnitScore = score
        output['yUnit'] = stdYUnit
        # return
        return output