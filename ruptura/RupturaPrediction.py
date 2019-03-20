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
        self.__walkCounter = 0
    
    def validate(self, Ytest, model):
        self.addFirstY(Ytest)
        scoreY = self._validationSteps(Ytest, model)
        self.plotScore(scoreY)
   
    def plotScore(self, scoreY):
        dataScore = []
        scorePred = self.getScore()
        for i in range(scoreY.shape[0]):
            for j in range(scoreY.shape[1]):
                dataScore.append([round(100*scorePred[i][j]), str(scoreY[i][j])])
        dataScore = pd.DataFrame(data=dataScore,columns=['score','Inadimplente'])
        de = DataExploration(dataScore)
        de.setNpoints(self.PLOT_POINTS)
        de.graphicInadimplenciaXContinuum(dataScore, 'score')  # MELHORAR ESSE GRAFICO
    
    def step(self, model):
        self.walk()
        annPrediction = model.predict(self.__X, batch_size=self.__X.shape[0], verbose=0)
        scoreBatch = self.calculateScoreOfBatch(annPrediction)
        self.__score.append(scoreBatch)

    def addFirstY(self, Ytest): # First Y is included in training batch, so we can use it for validation
        points = self.getStepPoints(Ytest,0)
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

    def calculateScoreOfBatch(self, pointsBatch, time_step = -1):
        points = self.getStepPoints(pointsBatch, time_step)
        score = []
        for point in points:
            score.append(point[1] + point[2])
        return score

    def _validationSteps(self,Ytest, model):
        scoreY = []
        for i in range(self.VALIDATION_DAYS):
            self.step(model)
            scoreY.append(self.calculateScoreOfBatch(Ytest,i+1))
        return np.array(scoreY)
    
    def _createDesconhecidoPoints(self):
        points = []
        for i in range(self.__X.shape[0]):
            points.append(self.DESCONHECIDO)
        return np.array(points) 
    