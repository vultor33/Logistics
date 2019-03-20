import pandas

class MachineLearningOptions:
    def __init__(self):
        """Class to handle user defined options\n
        WARNIN: check loadDatasetFromCsv to see options"""
        self.data = []
        self.targetColumn = -1
        self.__validationSize = 0.25
        self.__seed = 3
        self.__targetColumnIsNumber = False
        self.__crossValidationDataSplit = 10 # 10 is the general recommended value (date 09/18)
        self.__upSampleData = False
        self.__standarizeData = False
        self.__targetPercentage = '1'
        self.__variablesTransformationInfo = {}
        self.__columnsToSave = []
        self._setConstants()
        
    def loadDatasetFromCsv(self, fileName):
        self.data = pandas.read_csv(fileName,delimiter=';')

    def loadDatasetFromCsvLatin(self, fileName):
        self.data = pandas.read_csv(fileName,delimiter=';',encoding='latin-1',dtype=str)

    def setDataset(self, data):
        self.data = data

    def setVariablesTransformationInfo(self, value):
        self.__variablesTransformationInfo = value
        
    def getVariablesTransformationInfo(self):
        return self.__variablesTransformationInfo
        
    def setMLApplication(self, application):
        self.__ML_APPLICATION = application
        if application == self.__ML_APP_CLASSIFICATION:
            self.__scoring = 'accuracy'
        elif application == self.__ML_APP_REGRESSION:
            self.__scoring = 'r2'
        else:
            raise Exception(self.__ML_APP_ERROR)

    def getMLApplication(self):
        return self.__ML_APPLICATION

    def setTargetColumn(self, column):
        if len(self.data.columns) < column:
            raise Exception(self.__ML_TARGET_COLUMN_ERROR)
        self.targetColumn = column

    def setTargetPercentagePlot(self, targetPercentage):
        self.__targetPercentage = targetPercentage

    def getTargetPercentagePlot(self):
        return self.__targetPercentage

    def setValidationSize(self, value):
        self.__validationSize = value

    def getValidationSize(self):
        return self.__validationSize

    def setSeed(self, value):
        self.__seed = value
        
    def getSeed(self):
        return self.__seed

    def setTargetColumnIsNumber(self,value):
        self.__targetColumnIsNumber = value

    def getTargetColumnIsNumber(self):
        return self.__targetColumnIsNumber

    def setScoringMethod(self, value):
        self.__scoring = value

    def getScoringMethod(self):
        return self.__scoring

    def setCrossValidationDataSplit(self, value):
        self.__crossValidationDataSplit = value
    
    def getCrossValidationDataSplit(self):
        return self.__crossValidationDataSplit

    def setUpSampleData(self, value):
        self.__upSampleData = value
        
    def getUpSampleData(self):
        return self.__upSampleData

    def setStandarizeData(self, value):
        self.__standarizeData = value
        
    def getStandarizeData(self):
        return self.__standarizeData

    def setColumnsToSave(self, columns):
        self.__columnsToSave = columns

    def getColumnsToSave(self):
        return self.__columnsToSave

    def _setConstants(self):
        self.__ML_APP_CLASSIFICATION = 'classification'
        self.__ML_APP_REGRESSION = 'regression'
        self.__ML_APP_CLUSTERING = 'clustering'
        self.__ML_APP_ERROR = 'Application not implemented'
        self.__ML_TARGET_COLUMN_ERROR = 'Target column error - value greater than data length'

#################################################################################

if __name__ == "__main__":
    mlOptions = MachineLearningOptions()
    mlOptions.loadDatasetFromCsv('par_DATA.csv')
