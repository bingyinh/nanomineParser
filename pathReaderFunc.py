import csv

# currently has an encoding problem

def pathReader(path):
        pastUnits = {}
        pastTypes = {}
        
        # Find unique simplified values from all identical xpaths
        with open('typePath.csv', encoding='utf-8-sig', mode='r') as csv_unit:
            csv_reader = csv.reader(csv_unit)
            for row in csv_reader:
                if row[1] == path:
                    pastUnits[row[0]] = row[2]
                    
        with open('unitPath.csv', encoding='utf-8-sig', mode='r') as csv_unit:
            csv_reader = csv.reader(csv_unit)
            for row in csv_reader:
                if row[2] == path:
                    pastTypes[row[1]] = row[0]
                        
        return [pastUnits, pastTypes]
    
print(pathReader("properties/viscoelastic/dynamicproperties/dynamicpropertyprofile"))