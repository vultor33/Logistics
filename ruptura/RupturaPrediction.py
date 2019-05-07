import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from core.DataExploration import DataExploration

class RupturaPrediction:
    def __init__(self, X):
        self.DESCONHECIDO = [0,0,0,1]
        self.VALIDATION_DAYS = 7
        self.PLOT_POINTS = 5
        self.__Xstart = X.copy()
        self.__X = self.__Xstart.copy()
        self.__score = []
        self.__realValues = []
        self.__walkCounter = 0
    
    def getScore(self):
        return self.__score

    def getRealValues(self):
        return self.__realValues

    def getX(self):
        return self.__X
        
    def getWalkSteps(self):
        return self.__walkCounter
        
    def getLastPointsOfX(self):
        lastPoints = self.getStepPoints(self.__X,-1)
        return lastPoints
        
    def getStepPoints(self, pointsBatch, step_i, changeToArgmax = False):
        points = []
        for batch in pointsBatch:
            batchStep = batch[step_i]
            if changeToArgmax:
                value = np.argmax(batchStep)
                batchStep = np.zeros_like(batchStep)
                batchStep[value] = 1
            points.append(batchStep)
        return np.array(points)

    def plotScore(self, dataScore):
        dataScore.loc[:,'Inadimplente'] = [str(x) for x in dataScore.loc[:,'Inadimplente'].values]
        de = DataExploration(dataScore)
        de.setNpoints(self.PLOT_POINTS)
        de.graphicInadimplenciaXContinuum(dataScore, 'score')

    def plotAllBatches(self):
        for i_batch in range(self.__score.shape[1]):
            self.plotSampleOfBatch(i_batch)
    
    def plotSampleOfBatch(self, i_batch): #need to validate first
        if self.__walkCounter == 0:
            raise Exception('Cant plot sample, need to validate first')
        pred = self.__score[:,i_batch]
        real = self.__realValues[:,i_batch]
        x = range(len(pred))
        fig = plt.figure()
        name = 'amostra-' + str(i_batch) + '-previsto-vs-real'
        plt.title(name)
        plt.ylim((-0.1, 1.1))  
        plt.plot(x, pred, 'r', label='PREVISTO, x') # x
        plt.plot(x, real, 'b', label='REAL, y') # y
        plt.legend(loc='best')
        fig.savefig(name + '.png',dpi=150)
        plt.close(fig)
    
    def step(self, model):
        self.walk()
        annPrediction = model.predict(self.__X, batch_size=self.__X.shape[0], verbose=0)
        scoreBatch = self.calculateScoreOfBatch(annPrediction)
        self.__score.append(scoreBatch)

    def addLastX(self, lastX): # First Y is included in training batch, so we cant use it for validation
        self.walk(lastX)

    def walk(self, points = []):
        if len(points) == 0:
            points = self._createDesconhecidoPoints()
        Xnext = []
        for xBatch, point in zip(self.__X, points):
            xBatch = np.array(xBatch[1:])                   #throw first value
            Xnext.append(np.append(xBatch,[point],axis=0))  #add point
        self.__walkCounter += 1
        self.__X = np.array(Xnext)
        
    def _createDesconhecidoPoints(self):
        points = []
        for i in range(self.__X.shape[0]):
            points.append(self.DESCONHECIDO)
        return np.array(points) 

##############################################################################################
# VALIDATION
##############################################################################################
 
    def validate(self,Ytest, model):
        for i in range(self.VALIDATION_DAYS):
            self.step(model)
            self.__realValues.append(self.calculateScoreOfBatch(Ytest,i))
        self.__realValues = np.array(self.__realValues)
        self.__score = np.array(self.__score)
    
    def calculateDataScore(self):
        print('essa funcao depende muito do formato do Y')
        dataScore = []
        for i_batch in range(self.__realValues.shape[1]):
            predictions = []
            for day in range(self.__realValues.shape[0]):
                predictions.append(self.__score[day][i_batch])
                if self.__realValues[day][i_batch] != -1:
                    rupScore = int(100*np.max(predictions))
                    dataScore.append((rupScore,self.__realValues[day][i_batch]))
                    break
        dataScore = pd.DataFrame(data=dataScore,columns=['score','Inadimplente'])
        return dataScore
    
    def calculateScoreOfBatch(self, pointsBatch, time_step = -1):
        points = self.getStepPoints(pointsBatch, time_step)
        score = []
        for point in points:
            if point[1] == 1:
                score.append(-1)
            else:
                score.append(point[0])
        return score



