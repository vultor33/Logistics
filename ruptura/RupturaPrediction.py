import pandas as pd
import numpy as np
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
        
    def getScore(self):
        return np.array(self.__score)
        
    def getWalkSteps(self):
        return self.__walkCounter
        
    def getLastPointsOfX(self):
        lastPoints = rupPred.getStepPoints(self.__X,-1)
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
    
    def step(self, model):
        self.walk()
        annPrediction = model.predict(self.__X, batch_size=self.__X.shape[0], verbose=0)
        scoreBatch = self.calculateScoreOfBatch(annPrediction)
        self.__score.append(scoreBatch)

    def addFirstPrediction(self, Y): # First Y is included in training batch, so we cant use it for validation
        points = self.getStepPoints(Y,-1)
        self.walk(points)

    def walk(self, points = []):
        if len(points) == 0:
            points = self._createDesconhecidoPoints()
        Xnext = []
        for xBatch, point in zip(self.__X, points):
            xBatch = np.array(xBatch[1:])                   #throw first value
            Xnext.append(np.append(xBatch,[point],axis=0))  #add point
        self.__walkCounter += 1
        self.__X = np.array(Xnext)

    def calculateScoreOfBatch(self, pointsBatch, time_step = -1):
        points = self.getStepPoints(pointsBatch, time_step)
        score = []
        for point in points:
            score.append(point[1] + point[2])
        return score

    def validate(self,Ytest, model):
        yRealValues = []
        for i in range(self.VALIDATION_DAYS):
            self.step(model)
            self.__realValues.append(self.calculateScoreOfBatch(Ytest,i))
        self.__realValues = np.array(self.__realValues)
    
    def _createDesconhecidoPoints(self):
        points = []
        for i in range(self.__X.shape[0]):
            points.append(self.DESCONHECIDO)
        return np.array(points) 

    def calculateDataScore(self):
        dataScore = []
        for i_batch in range(self.__realValues.shape[1]):
            predictions = []
            isRuptura = False
            for day in range(self.__realValues.shape[0]):
                predictions.append(self.__score[day][i_batch])
                if self.__realValues[day][i_batch] == 1:
                    rupScore = int(100*np.median(predictions))
                    dataScore.append((rupScore,1))
                    isRuptura = True
                    break
            if not isRuptura:
                rupScore = int(100*np.median(predictions))
                dataScore.append((rupScore,0))   
        dataScore = pd.DataFrame(data=dataScore,columns=['score','Inadimplente'])
        return dataScore



