import json
import pandas
from core.util import cleanDataColumns
from core.FeatureTransform import FeatureTransform

class JsonTransforms:
    def __init__(self, version, deploy = False):
        self.__REFERENCE_DATE = ' Data'
        self.__TARGET_COLUMN = 'Inadimplente'
        self.__TITLE = 'SmartCredit-' 
        self.__deploy = deploy
        self.__version = version
            
    def save(self, options):
        if self.__deploy:
            options = self._removeOutliersMarkers(options)
        version = self.getVersion()
        with open(self.__TITLE + version + '.json', 'w') as outfile:
            json.dump(options, outfile)
            
    def load(self):
        version = self.getVersion()
        with open(self.__TITLE + version + '.json') as f:
            options = json.load(f)
        return options
    
    def transformTable(self, fileName):
        data, featT = self._cleanTable(fileName)
        options = self.load()
        for colName in options:
            data = featT.transform(data, colName,options)
        columnNames = featT.getAllColumnsNames(options)
        if self.__TARGET_COLUMN in data.columns:
            data = data.loc[:, columnNames + [self.__TARGET_COLUMN]]
        else:
            data = data.loc[:, columnNames]
        return data
    
    def saveTransformedTable(self, fileName):
        data, featT = self._cleanTable(fileName)
        options = self.load()
        for colName in options:
            data = featT.transform(data, colName,options)
        columnNames = featT.getAllColumnsNames(options)
        data = data.loc[:, columnNames + [self.__TARGET_COLUMN]]
        version = self.getVersion()
        saveName = self.__TITLE + version + '-table.csv'
        data.to_csv(saveName,sep=';')
        print('saved as ',saveName)
        
    def loadTable(self):
        version = self.getVersion()
        fileName = self.__TITLE + version + '-table.csv'
        data = pandas.read_csv(fileName,delimiter=';',encoding='latin-1',dtype=str)
        data = data.drop('Unnamed: 0',axis=1)
        return data

    def optionsToDeploy(self):
        self.__deploy = False
        options = self.load()
        self.__deploy = True
        self.save(options)

    def getVersion(self):
        version = self.__version
        if self.__deploy:
            version += '-deploy'
        return version

    def _cleanTable(self, fileName):
        data = pandas.read_csv(fileName,delimiter=';',encoding='latin-1',dtype=str)
        data = cleanDataColumns(data)
        featT = FeatureTransform()
        featT.setDateReference(data.loc[:,' Data']) # convert date to days
        return [data, featT]    

    def _removeOutliersMarkers(self, options):
        outlier = 'outliersCut'
        transforms = 'transforms'
        for option in options:
            if outlier in options[option][transforms]:
                options[option][transforms][outlier] = [None,None]
        return options
        
        