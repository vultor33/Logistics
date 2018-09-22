import pandas

class MachineLearningOptions:

	def __init__(self):
		"""Class to handle user defined options"""
		self.data = []
		self.targetColumn = -1

		self.__validationSize = 0.25
		self.__seed = 3
		self.__targetColumnIsNumber = True
		self._setConstants()
		self.__crossValidationDataSplit = 10 # 10 is the general recommended value (date 09/18)

	def loadDatasetFromCsv(self, fileName):
		self.data = pandas.read_csv(fileName,delimiter=';')

	def setDataset(self, data):
		self.data = data

	def setMLApplication(self, application):
		if application == self.__ML_APP_CLASSIFICATION:
			self.__scoring = 'accuracy'
		elif application == self.__ML_APP_REGRESSION:
			self.__scoring = 'r2'
		else:
			raise Exception(self.__ML_APP_ERROR)

	def getMLApplication(self):
		return self.__ML_APPLICATION

	def setTargetColumn(self, column):
		if len(self.data) < column:
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
		
	def setCrossValidationDataSplit(self, value):
		self.__crossValidationDataSplit = value

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
		
	
	
	
