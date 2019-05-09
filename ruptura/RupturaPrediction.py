import numpy as np

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
        self.reshapeAnnPred()
        return self.getAnnPred()
    
    def step(self, model):
        self._advanceX()
        annPrediction = model.predict(self.__X, batch_size=self.__X.shape[0], verbose=0)
        lastDayPredicted = self.getLastDay(annPrediction)
        self.__annPred.append(lastDayPredicted) # cada passo eu quero a previsao do proximo (ultimo) ponto

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

    def reshapeAnnPred(self):
        self.__annPred = np.array(self.__annPred)
        predNew = []
        for i_batch in range(self.__annPred.shape[1]):
            daysPred = []
            for day in range(self.__annPred.shape[0]):
                daysPred.append(self.__annPred[day][i_batch])
            predNew.append(daysPred)
        self.__annPred = np.array(predNew)

    def getX(self):
        return self.__X
    
    
    
    