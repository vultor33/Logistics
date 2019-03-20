import numpy as np
from sklearn import linear_model
from sklearn.svm import SVR
from sklearn.kernel_ridge import KernelRidge
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPRegressor
from sklearn import model_selection
from AlgorithmsEvaluation import AlgorithmsEvaluation

from MachineLearningOptions import MachineLearningOptions

# multivariate input
X = [[0., 0.], [1., 1.], [2., 2.], [3., 3.]]
# univariate output
Y = [0., 1., 2., 3.]
# multivariate output
Z = [[0., 1.], [1., 2.], [2., 3.], [3., 4.]]
#
## ordinary least squares
#clf = linear_model.LinearRegression()
## univariate
#clf.fit(X, Y)
#print('linear:  ',clf.predict ([[1, 0.]]))
#
## Ridge
#clf = linear_model.BayesianRidge()
## univariate
#clf.fit(X, Y)
#print('bayesian:  ',clf.predict ([[1, 0.]]))
#
#svr = GridSearchCV(SVR(kernel='rbf', gamma=0.1), cv=2,
#                   param_grid={"C": [1e0, 1e1, 1e2, 1e3],
#                               "gamma": np.logspace(-2, 2, 5)})
#
#kr = GridSearchCV(KernelRidge(kernel='rbf', gamma=0.1), cv=2,
#                  param_grid={"alpha": [1e0, 0.1, 1e-2, 1e-3],
#                              "gamma": np.logspace(-2, 2, 5)})
#kfCv = 2
#
#mlp = MLPRegressor()
#param_grid = {'hidden_layer_sizes': [i for i in range(1,15)],
#              'activation': ['relu'],
#              'solver': ['adam'],
#              'learning_rate': ['constant'],
#              'learning_rate_init': [0.001],
#              'power_t': [0.5],
#              'alpha': [0.0001],
#              'max_iter': [1000],
#              'early_stopping': [False],
#              'warm_start': [False]}
#mlp = GridSearchCV(mlp, param_grid=param_grid,
#                   cv=kfCv, verbose=False, pre_dispatch='2*n_jobs', scoring='r2')
## Ridge
#clf = svr
## univariate
#clf.fit(X, Y)
#print('support vector machine:  ',clf.predict ([[1, 0.]]))
#
## Ridge
#clf = kr
## univariate
#clf.fit(X, Y)
#print('kernel:  ',clf.predict ([[1, 0.]]))
#
## Ridge
#clf = mlp
## univariate
#clf.fit(X, Y)
#print('ANN:  ',clf.predict ([[1, 0.]]))
#
#
#
#crossValidationDivisions = model_selection.KFold(
#               n_splits=2,
#			   random_state=3)
#        
#crossValidationResults = model_selection.cross_val_score(
#		clf, 
#		X,
#		Y, 
#		cv=crossValidationDivisions,
#		scoring='r2')
#        
#result = [crossValidationResults.mean(),crossValidationResults.std()]
#print(result)
 
# multivariate input
X = [[0., 0.], [1., 1.], [2., 2.], [3., 3.]]
# univariate output
Y = [0., 1., 2., 3.]
# DEFINING OPTIONS - par_DATA
mlOptions = MachineLearningOptions()
mlOptions.setMLApplication('regression')
mlOptions.setCrossValidationDataSplit(2)

algoz = AlgorithmsEvaluation(X,Y,mlOptions)
algoz.runDefaultTest()








