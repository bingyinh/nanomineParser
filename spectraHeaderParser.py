# skeleton of the big parser class
import csv
from lxml import etree
from standardizer import standardizer
import re

class spectraHeaderParser(object):
    # init function
    def __init__(self):
        # initialize subclasses
        self.standardizers = self.__loadSC__()
        pass

    # header separator function (TODO)
    def separator(self, xheader, yheader):
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
        # predefined xpath-subclass pairs, fill in the rest (TODO)
        xpathSubclassPairs = {
            'PROPERTIES/Viscoelastic/DynamicProperties/DynamicPropertyProfile': {
                'xName': {
                    self.frequency,
                    self.temperature,
                    self.strain
                },
                'xUnit': {
                    self.frequencyUnit,
                    self.temperatureUnit,
                    self.strainUnit,
                    self.dimensionless
                },
                'yName': {
                    self.storageModulus,
                    self.lossModulus,
                    self.tanDelta,
                    self.normalizedStorageModulus,
                    self.normalizedLossModulus,
                    self.normalizedTanDelta,
                    self.shearStorageModulus,
                    self.shearLossModulus
                },
                'yUnit': {
                    self.modulusUnit,
                    self.dimensionless
                }
            }
        }
        # remove brackets from xpath
        noBracketXpath = re.sub(r'\[.*?\]','',xpath)
        return xpathSubclassPairs[noBracketXpath]

    # preload subclasses
    def __loadSC__(self):
        '''
        Load standard/non-standard name pairs and load subclasses with those pairs
        '''
        ## subclass section
        # For DynamicPropertyProfiles, the following subclasses are needed:
        #     ----------------------
        #     Storage Modulus
        #     Loss Modulus
        #     Tan Delta
        #     Normalized Storage Modulus
        #     Normalized Loss Modulus
        #     Normalized Tan Delta
        #     Shear Storage Modulus
        #     Shear Loss Modulus
        #     ----------------------
        #     Temperature
        #     Frequency (including Angular Frequency)
        #     Strain
        #     ----------------------
        #     TemperatureUnit (Celsius, Kelvin)
        #     FrequencyUnit (Hz, rad/s)
        #     StrainUnit (%?)
        #     ModulusUnit (Pa, MPa, GPa...)
        
        # these name pairs should be read from an external file in the future (something like your pathReaderFunc.py), fill in for the rest of the needed subclasses (TODO)
        namePairs = {
            'Storage Modulus': {
                "E'",
                'Normalized Storage Modulus',
                "Storage Modulus, E'",
                "Storage Modulus E'",
                'Storage Modulus',
                "Log E'",
                'Log storage modulus',
                'Storage modulus',
                'Storage Modulu',
                'Log-storage modulus',
                'Storage Modulus, E',
                'storage modulus'
            },
            'Loss Modulus': {
                'E"',
                "E''",
                'loss modulus',
                'Loss modulu',
                'e"',
                'Loss modulus',
                'Loss Modulus',
                "Log(loss factor e'')"
            },
            'Celsius': {
                '*C',
                '°c',
                'c',
                'c*',
                'cel',
                'cel.',
                'celsius',
                'deg C',
                'Deg. Celcius',
                '°C'
            },
            'Kelvin': {
                'K',
                'kelvin'
            }
        }
        self.storageModulus = standardizer({'Storage Modulus': namePairs['Storage Modulus']})
        self.lossModulus = standardizer({'Loss Modulus': namePairs['Loss Modulus']})
        self.temperatureUnit = standardizer({'Celcius': namePairs['Celsius'], 'Kelvin': namePairs['Kelvin']})

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
        # init output
        output = {
            'xName': None,
            'xUnit': None,
            'yName': None,
            'yUnit': None
        }
        # separate headers
        xName, xUnit, yName, yUnit = self.separator(xheader, yheader)
        # read xpath to determine subclasses
        subclassPools = self.xpathReader(xpath)
        # for cases where multiple paired subclasses, need something to determine which one to use, for now we just assume only the correct subclass will return a string while other subclasses will return None (TODO)
        # standardize xName
        stdXName = None
        for subclass in subclassPools['xName']:
            stdXName = stdXName or subclass.evaluate(xName)
        output['xName'] = stdXName
        # standardize xUnit
        stdXUnit = None
        for subclass in subclassPools['xUnit']:
            stdXUnit = stdXUnit or subclass.evaluate(xUnit)
        output['xUnit'] = stdXUnit
        # standardize yName
        stdYName = None
        for subclass in subclassPools['yName']:
            stdYName = stdYName or subclass.evaluate(yName)
        output['yName'] = stdYName
        # standardize yUnit
        stdYUnit = None
        for subclass in subclassPools['yUnit']:
            stdYUnit = stdYUnit or subclass.evaluate(yUnit)
        output['yUnit'] = stdYUnit
        # return
        return output