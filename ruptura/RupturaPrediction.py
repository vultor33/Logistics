import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from core.DataExploration import DataExploration

# The neural network receives 60 and returns the next point of each of received point.
# X = [dia 1 - presenca, dia 2 - desconhecido, dia 3 - ruptura]
# Y = [dia 2 - desconhecido, dia 3 - ruputura, dia 4 - deconhecido] (so tenho interesse nesse dia 4)

class RupturaPrediction:
    def __init__(self, X, xUnknow):
        self.UNKNOW = xUnknow
        self.VALIDATION_DAYS = 7
        self.PLOT_POINTS = 5
        self.walkCounter = 0
        self.__X = X.copy()
        self.__annPred = []

        
##############################################################################################
# BATCH CUTS
##############################################################################################
        
    def returnSelectedDayBatch(self, pointsBatch, selectedDay):
        """
        Receives a pointsBatch in following format: 
        (N samples of client-product , days around 60, one hot encoder representing event)
        Returns in following format of the selectedDay:
        (N samples of client-product , one hot encoder representing event)
        """
        points = []
        for batch in pointsBatch:
            batchStep = batch[selectedDay]
            points.append(batchStep)
        return np.array(points)

    def getLastDay(self, pointsBatch):
        return self.returnSelectedDayBatch(pointsBatch, -1)

    def applyArgMaxToSelectedDayBatch(self, dayBatch):
        eventSize = dayBatch.shape[1]
        eventsArgMax = []
        for event in dayBatch:
            argM = np.argmax(event)
            event = np.zeros(eventSize)
            event[argM] = 1
            eventsArgMax.append(event)
        return np.array(eventsArgMax)

##############################################################################################
# WALK IN THE PREDICTIONS
##############################################################################################
    
    def walkNSteps(self, model, nSteps):
        for i in range(nSteps):
            self.step(model)
        return self.getAnnPred()
    
    def step(self, model):
        self._advanceX()
        annPrediction = model.predict(self.__X, batch_size=self.__X.shape[0], verbose=0)
        self.__annPred.append(self.getLastDay(annPrediction)) # cada passo eu quero a previsao do proximo (ultimo) ponto

    def _advanceX(self, points = []):
        if len(points) == 0:
            points = self._createUnknowPoints()
        Xnext = []
        for xBatch, point in zip(self.__X, points):
            xBatch = np.array(xBatch[1:])                   #throw first value
            Xnext.append(np.append(xBatch,[point],axis=0))  #add point
        self.walkCounter += 1
        self.__X = np.array(Xnext)

    def _createUnknowPoints(self):
        points = []
        for i in range(self.__X.shape[0]):
            points.append(self.UNKNOW)
        return np.array(points) 
        
    def addLastX(self, lastX): # First Y is included in training batch, so we cant use it for validation
        self._advanceX(lastX)


##############################################################################################
# GETTERS
##############################################################################################

    def getAnnPred(self):
        return np.array(self.__annPred)

    def getX(self):
        return self.__X
    
    
    
    
    
    
    
    
    
    
    
    
    
##############################################################################################
# SCORE
##############################################################################################

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



