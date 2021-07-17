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
            'Tan Delta': {
                'loss tangent',
                'Bending Tan delta',
                'Dielectric Loss Tangent',
                'Dielctric Loss Factor',
                'Dielectric loss',
                'Tan d',
                'Tan del',
                'Damping Factor',
                'Tan δ',
                'Dissipation Factor',
                'tangent delta',
                'Tan delta',
                'Log Tan delta',
                'loss factor',
                'Loss factor',
                'Damping factor',
                'Damping Coefficient',
                'Loss Tangent',
                'tan del',
                'dielectric loss tangent',
                'Permittivity',
                'Effective dielectric constant',
                'tan delta',
                'Tan',
                'dissipation factor',
                'Tangent Delta',
                'Tan Delta',
                'loss tanget',
                'tanδ',
                'Loss tangent',
                'Dissipation factor',
                'Dielectric Loss',
                'dielectric loss',
                'dielectric loss, tangent',
                'Dielectric Loss Factor',
                'Effective dielectric loss'
            },
            'Normalized Storage Modulus': {
                "E'/E'max"
            },
            'Normalized Loss Modulus': {
                'E"/E"max'
            },
            'Normalized Tan Delta': {
                'normalized tan delta'
            },
            'Shear Storage Modulus': {
                'Shear Storage Modulus',
                "Storage Modulus, G'",
                'shear storage modulus',
                "G'",
                'Shear storage modulus G'
            },
            'Shear Loss Modulus': {
                "Loss Modulus, G''",
                'Shear Loss Modulus',
                "G''",
                'G"'
            },
            'Temperature': {
                'Temperatur',
                'Temperature',
                'Temp',
                'T',
                'Tempeature',
                'temperature'
            },
            'Frequency': {
                'Fequency',
                'f',
                'Frequency',
                'Frequecy',
                'Log f',
                'Angular velocity',
                'freq/Hz',
                'Oscillation frequency, ω',
                'Angular Frequency',
                'w',
                'Frequenc',
                'Freq',
                'Angular frequency',
                'freq',
                'ang. frequency',
                'frequency',
                'Angular Velocity'
            },
            'Strain': {
                'strain',
                'strain rate',
                'Critical strain',
                'Hencky strain',
                'Static Strain',
                'Failure Strain',
                'strain to failure'
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
            },
            'Hz': {
                'Hertz',
                'Hz'
            },
            'kHz': {
                '1000 Hz',
                '*10^3 Hz'
            },
            'MHz': {
                '1000000 Hz'
                '*10^6 Hz'
            },
            'GHz': {
                '1000000000 Hz'
                '*10^9 Hz'
            },
            'rad/s': {
                'rad/sec',
                'rad/second'
            },
            '%': {
                'percent'
            },
            'Pa': {
                'Pascal'
            },
            'kPa': {
                '1000 Pa',
                '1000 Pascal',
                '*10^3 Pa'
            },
            'MPa': {
                '1000000 Pa',
                '1000000 Pascal',
                '*10^6 Pa'
            },
            'GPa': {
                '1000000000 Pa',
                '1000000000 Pascal',
                '*10^9 Pa'
            },
            '(dimensionless)': {
                'dimensionless'
            }
        }
        self.storageModulus = standardizer({'Storage Modulus': namePairs['Storage Modulus']})
        self.lossModulus = standardizer({'Loss Modulus': namePairs['Loss Modulus']})
        self.tanDelta = standardizer({'Tan Delta': namePairs['Tan Delta']})
        self.normalizedStorageModulus = standardizer({'Normalized Storage Modulus': namePairs['Normalized Storage Modulus']})
        self.normalizedLossModulus = standardizer({'Normalized Loss Modulus': namePairs['Normalized Loss Modulus']})
        self.normalizedTanDelta = standardizer({'Normalized Tan Delta': namePairs['Normalized Tan Delta']})
        self.shearStorageModulus = standardizer({'Shear Storage Modulus': namePairs['Shear Storage Modulus']})
        self.shearLossModulus = standardizer({'Shear Loss Modulus': namePairs['Shear Loss Modulus']})
        self.temperature = standardizer({'Temperature': namePairs['Temperature']})
        self.frequency = standardizer({'Frequency': namePairs['Frequency']})
        self.strain = standardizer({'Strain': namePairs['Strain']})
        self.temperatureUnit = standardizer({'Celsius': namePairs['Celsius'], 'Kelvin': namePairs['Kelvin']})
        self.frequencyUnit = standardizer({'Hz': namePairs['Hz'], 'kHz': namePairs['kHz'], 'MHz': namePairs['MHz'], 'GHz': namePairs['GHz'], 'rad/s': namePairs['rad/s']})
        self.strainUnit = standardizer({'%': namePairs['%']})
        self.modulusUnit = standardizer({'Pa': namePairs['Pa'], 'kPa': namePairs['kPa'], 'MPa': namePairs['MPa'], 'GPa': namePairs['GPa']})
        self.dimensionless = standardizer({'(dimensionless)': namePairs['(dimensionless)']})
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

if __name__ == '__main__':
    shp = spectraHeaderParser()
    # test case 1
    xpath = 'PROPERTIES/Viscoelastic/DynamicProperties/DynamicPropertyProfile'
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
        'yUnit':'(dimensionless)'
    }
    print(shp.parse(xpath, xheader, yheader))
    assert shp.parse(xpath, xheader, yheader) == answer, 'Fail test case 2'
    print("All tests passed")