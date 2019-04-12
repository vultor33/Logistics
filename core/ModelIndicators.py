import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
from sklearn.model_selection import train_test_split

from core.SmartCreditModel import SmartCreditModel
from core.JsonTransforms import JsonTransforms

class ModelIndicators:
    def __init__(self, version):
        self.TARGET_COLUMN = 'Inadimplente'
        self.TARGET_TRUE_FLAG = 1
        self.TARGET_FALSE_FLAG = 0
        self.TARGET_SCORE_CUT = 0.5
        self.RANDOM_STATE_SPLIT = 30
        self.__CONFUSION_PLOT_NAME = 'confusionPlot-' + version + '.png'
        self.__ROC_PLOT_NAME = 'rocPlot-' + version + '.png'
        self.__deploy = False
        self.__version = version

    def setPredProbs(self, Y, PRED):
        self.__pred = PRED
        self.__predValues = [self._isTargetTrue(x) for x in self.__pred]
        self.__ytrue  = Y

    def _isTargetTrue(self, predProb):
        return 1 if predProb > self.TARGET_SCORE_CUT else 0
    
    def getY(self):
        return self.__ytrue
        
    def getPredProbs(self):
        return self.__pred

    def getPredValues(self):
        return self.__predValues

        
#######################################################################################################################
# INDICATORS
#######################################################################################################################

    def allIndicators(self):
        indic = []
        indic.append(self.accuracy())
        indic.append(self.detectionErrors())
        indic.append(self.precisionTarget())
        indic.append(self.recallTarget())
        indic.append(self.f1())
        indic.append(self.cohenKappa())
        indic.append(self.roc())
        indic = pd.DataFrame(data=indic)
        indic.columns = ['Model']
        indic.index = ['accuracy', 'detectionErrors','precision', 'recall','F1','Kappa', 'ROC']
        return indic

    def accuracy(self):
        return metrics.accuracy_score(self.__ytrue, self.__predValues)

    def detectionErrors(self):
        conf = self.confusionMatrix()
        return conf[1][0]/(conf[1][0] + conf[0][0])

    def precisionTarget(self):
        return metrics.precision_score(self.__ytrue, self.__predValues, pos_label=self.TARGET_TRUE_FLAG)

    def recallTarget(self):
        return metrics.recall_score(self.__ytrue, self.__predValues, pos_label=self.TARGET_TRUE_FLAG)
    
    def f1(self):
        return metrics.f1_score(self.__ytrue, self.__predValues, pos_label=self.TARGET_TRUE_FLAG)
    
    def cohenKappa(self):
        return metrics.cohen_kappa_score(self.__ytrue, self.__predValues)
    
    def confusionMatrix(self):
        cMatrix = metrics.confusion_matrix(self.__ytrue, self.__predValues, 
                       labels = [self.TARGET_FALSE_FLAG, self.TARGET_TRUE_FLAG])
        return cMatrix

    
    def plotConfusionMatric(self):
        conf = self.confusionMatrix()
        fig = plt.figure()
        seaPlotTrain = sns.heatmap(conf, square=True, annot=True, cbar=False)
        plt.xlabel('PREDICTED')
        plt.ylabel('TRUE')
        fig.savefig(self.__CONFUSION_PLOT_NAME,dpi=150)    
        plt.close(fig)
    
#######################################################################################################################
# PROBABILITIES INDICATORS
#######################################################################################################################

    def roc(self):
        rocValue, _, _ = self._rocIndicator(self.__ytrue, self.__pred)
        return rocValue

    def _rocIndicator(self, y, predProba):
        fpr, tpr, _ = metrics.roc_curve(y, predProba)
        roc_auc = metrics.auc(fpr, tpr)
        return [roc_auc, fpr, tpr]    

    def plotRoc(self): 
        fig = plt.figure()
        rocValue, fpr, tpr = self._rocIndicator(self.__ytrue, self.__pred)
        self._plotRocCurve(rocValue, fpr, tpr)
        fig.savefig(self.__ROC_PLOT_NAME,dpi=150)    
        plt.close(fig)
  
    def _plotRocCurve(self, roc_auc, fpr, tpr):
        plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
        plt.legend(loc = 'lower right')
        plt.plot([0, 1], [0, 1],'r--')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
    
    
##################################################################################################################
# SmartCredit
##################################################################################################################
        
    def train(self):
        data = self.readData()
        train, test = self._breakIntoTrainAndTest(data)
        XY = self._breakIntoXandY(train, test)
        self._trainModel(XY)

    def readData(self):
        jsonTransforms = JsonTransforms(self.__version, self.__deploy)
        return jsonTransforms.loadTable()
        
    def bootstrap(self, data):
        train, test = self._breakIntoTrainAndTest(data)
        train = self._resampleData(train)
        test = self._resampleData(test)
        XY = self._breakIntoXandY(train, test)
        self._trainModel(XY)

    def _breakIntoTrainAndTest(self, data):
        train, test = train_test_split(data, test_size=0.2, random_state = self.RANDOM_STATE_SPLIT)
        train = train.reset_index(drop=True)
        test = test.reset_index(drop=True)
        return [train, test]

    def _resampleData(self, data):
        resampleIndexes = []
        nLimit = len(data)-1
        for i in data.index:
            iRand = random.randint(0,nLimit)
            resampleIndexes.append(iRand)
        resampleData = data.loc[resampleIndexes,:].copy()
        resampleData = resampleData.reset_index(drop=True)
        return resampleData
        
    def _breakIntoXandY(self, train, test):
        xtrain = train.drop([self.TARGET_COLUMN],axis=1)
        xtest = test.drop([self.TARGET_COLUMN],axis=1)
        ytrain  = train.loc[:,self.TARGET_COLUMN].copy()
        ytrain = [int(x) for x in ytrain]
        ytest = test.loc[:,self.TARGET_COLUMN].copy()
        ytest = [int(x) for x in ytest]
        X = [xtrain, xtest]
        Y = [ytrain, ytest]
        return [X, Y]
        
    def _trainModel(self, XY):
        X,Y = XY
        xtrain, xtest = X
        ytrain, ytest  = Y
        scModel = SmartCreditModel(self.__version, self.__deploy)
        model = scModel.untrained()
        model.fit(xtrain, ytrain)
        predProbsTrain = model.predict_proba(xtrain)
        predProbsTest = model.predict_proba(xtest)
        PRED = [predProbsTrain, predProbsTest]
        self.setPredProbs(Y, PRED)

    
    
    