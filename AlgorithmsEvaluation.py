import numpy
from sklearn import model_selection
from sklearn.model_selection import GridSearchCV
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVR
from sklearn.kernel_ridge import KernelRidge
from sklearn.neural_network import MLPRegressor

class AlgorithmsEvaluation:

	def __init__(self, X_train, Y_train):
        #e necessario implementar o GridSearchCV que e mais preciso
		self.__SEED = 7
		self.__SCORING = 'accuracy'
		self.__DATASETSPLIT = 10 # 10 is the general recommended value (date 09/18) tem o leave one out cross validation q e com tudo, mas deve ser bem mais pesado - fazer com o modelo final
		self.__X_train = X_train
		self.__Y_train = Y_train

	def setCrossValidationSplitNumber(self, value):
		self.__DATASETSPLIT = value
		
	def setScoringMethod(self, value):
		self.__SCORING = value

	def runTest(self):
		models = self._defaultModels()
		bestModel = models[0]
		bestModelFit = -1
		for name, model in models:
			modelType = [name, model]
			numberResult = self.evaluateMethod(model)
			self._printResults(modelType + numberResult)
			if(numberResult[0] > bestModelFit):
				bestModel = modelType
				bestModelFit = numberResult[0]
		return bestModel

	def runTestRegression(self):
		self.__evaluationResults = open('AlgorithmEvaluation.txt','w')
		models = self._defaultRegressionModels()
		bestModel = models[0]
		bestModelFit = -1
		for name, model in models:
			modelType = [name, model]
			numberResult = self.evaluateMethod(model)
			self._printResults(modelType + numberResult)
			if(numberResult[0] > bestModelFit):
				bestModel = modelType
				bestModelFit = numberResult[0]
		self.__evaluationResults.close()
		return bestModel
   
	def evaluateMethod(self, method):
		crossValidationDivisions = model_selection.KFold(
				n_splits=self.__DATASETSPLIT, 
				random_state=self.__SEED)
        
		crossValidationResults = model_selection.cross_val_score(
				method, 
				self.__X_train,
				self.__Y_train, 
				cv=crossValidationDivisions, 
				scoring=self.__SCORING)
        
		result = [crossValidationResults.mean(),crossValidationResults.std()]
		return result

	def _defaultModels(self):
		models = []
		#clf1 = LogisticRegression()
		#clf2 = RandomForestClassifier()
		#clf3 = GaussianNB()
		#vot = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)], voting='hard')
		#models.append(('VOT',vot))
		#models.append(('PER', Perceptron()))
		models.append(('SGD', SGDClassifier()))
		#models.append(('GPM',GaussianProcessClassifier())) # ESSE CARA E CARO - MAS DEU 100%
		models.append(('ADA',AdaBoostClassifier()))
		#models.append(('ANN', MLPClassifier()))
		#models.append(('GBC',GradientBoostingClassifier()))
		models.append(('LOG', LogisticRegression()))
		#models.append(('LDA', LinearDiscriminantAnalysis()))
		models.append(('KNN', KNeighborsClassifier()))
		#models.append(('CART', DecisionTreeClassifier()))
		#models.append(('NB', GaussianNB()))
		#models.append(('SVM', SVC()))
		models.append(('RFC',RandomForestClassifier(max_depth=2, random_state=0)))
		return models

	def _defaultRegressionModels(self):
		models = []
		models.append(('LREG', linear_model.LinearRegression()))
		models.append(('BAY', linear_model.BayesianRidge()))
		svr = GridSearchCV(SVR(kernel='rbf', gamma=0.1), cv=self.__DATASETSPLIT, scoring='r2',
					 param_grid={"C": [1e0, 1e1, 1e2, 1e3],"gamma": numpy.logspace(-2, 2, 5)})
		models.append(('SVR', svr))
		kr = GridSearchCV(KernelRidge(kernel='rbf', gamma=0.1), cv=self.__DATASETSPLIT, scoring='r2',
					param_grid={"alpha": [1e0, 0.1, 1e-2, 1e-3],"gamma": numpy.logspace(-2, 2, 5)})
		models.append(('KR', kr))
		mlp = MLPRegressor()
		param_grid = {'hidden_layer_sizes': [i for i in range(1,15)],
              'activation': ['relu'],
              'solver': ['adam'],
              'learning_rate': ['constant'],
              'learning_rate_init': [0.001],
              'power_t': [0.5],
              'alpha': [0.0001],
              'max_iter': [1000],
              'early_stopping': [False],
              'warm_start': [False]}
		mlp = GridSearchCV(mlp, param_grid=param_grid,
                   cv=self.__DATASETSPLIT, verbose=False, pre_dispatch='2*n_jobs', scoring='r2')
		
		
		
		return models
        

	def _printResults(self, result):
		msg = "Accuracy: %0.2f (+/- %0.2f)" % (result[2], 2*result[3])
		self.__evaluationResults.write(result[0] + "  " + msg + '\n')
    

#############################################################################################################################
    
if __name__ == "__main__":
    print("AlgorithmsEvalutaion module")    
    
    
        
    