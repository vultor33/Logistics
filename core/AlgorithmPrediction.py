from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import tree
import graphviz

class AlgorithmPrediction:
    
    def __init__(self, method, dataPrepared):
        """ Example of use: \n
        algoPred = fitModel(DataPreparation, method)\n
        algoPred.testDataPrediction()\n
        """
        self.__confusionMatrix = []
        self.__method = method
        self.__dataPrepared = dataPrepared
        self.__method.fit(self.__dataPrepared.getXtrain(), self.__dataPrepared.getYtrain())
        self.__predictionErrorPercentage = 0

    def getMethod(self):
        return self.__method

    def getPredictionErrors(self):
        return self.__predictionErrors

    def getConfusionMatrix(self):
        return self.__confusionMatrix

    def getPredictionError(self):
        return self.__predictionErrorPercentage

    def testDataPrediction(self):
        predictions = self.__method.predict(self.__dataPrepared.getXtest())
        self._avaliatePredictions(self.__dataPrepared, predictions)

    def predictNewData(self, data):
        return self.__method.predict(data)

    def _avaliatePredictions(self, dp, predictions):
        self.__predictionErrors = []
        for i in range(len(predictions)):
            if predictions[i] != dp.getYtest()[i]:
                self.__predictionErrors.append(i)
        self.__predictionErrorPercentage = 100*len(self.__predictionErrors)/len(self.__dataPrepared.getXtest())
        print("nE:  ",self.__predictionErrorPercentage)
        self._confusionPlot(self.__dataPrepared.getYtest(), predictions)
		
    def _confusionPlot(self, Ytest, predictions):
        self.__confusionMatrix = confusion_matrix(Ytest, predictions)
        seaPlot = sns.heatmap(self.__confusionMatrix, square=True, annot=True, cbar=False)
        plt.xlabel('predicted value')
        plt.ylabel('true value')
        fig = seaPlot.get_figure()
        fig.savefig('confusion-plot', dpi=150)
        plt.close(fig)

    def plotTreeClassifierGraph(self):
        featureNames = self.__dataPrepared.getFeaturesNames()
        dot_data = tree.export_graphviz(
                self.__method,
                out_file=None, 
                feature_names=featureNames)
                #class_names=classNames) can add class names here
        graph = graphviz.Source(dot_data)
        graph.render("treeClassifierGraphic")
        
