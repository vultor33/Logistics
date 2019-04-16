import datetime

class Encoder:
    def __init__(self, version):
        self.__version = version
        self.TEST_DAYS = 7
        self.__now = datetime.datetime.now()

    def applyOneHotEncoder(self, sample, referenceDate):
        allSamples = {}
        for client in sample:
            if not self._checkClient(sample, client):
                continue
            xSample, lastX = self._defineX(sample, client, referenceDate)  #try sample[client]
            ySample = self._defineY(xSample, sample, client, referenceDate)
            yTest = self._defineYTest(sample, client, referenceDate)
            encodedSample = self._encodeSample(client, xSample, ySample, yTest, lastX)
            allSamples.update(encodedSample)
        return allSamples

    def _defineX(self, sample, client, referenceDate):
        x1, x2 = self.defineTrainWindowDates(referenceDate)
        xSample = []
        for date in range(x1,x2):
            event = self._getXEvent(date, sample, client)
            xSample.append(event)
        lastX = self._getXEvent(x2, sample, client)
        return [xSample, lastX]
    
    def _getXEvent(self, date, sample, client):
        if date in sample[client]['data']:
            dateIndex = sample[client]['data'].index(date)
            event = list(sample[client]['x'][dateIndex])
            event.append(0) # UNKNOW = False
        else:
            size = len(sample[client]['x'][0])
            event = [0*x for x in range(size)]
            event.append(1)
        return event

    def _defineY(self, xSample, sample, client, referenceDate):
        _, x2 = self.defineTrainWindowDates(referenceDate)
        ySample = list(xSample)
        ySample.pop(0)
        ySample = [self._calculateYEventFromX(xEvent) for xEvent in ySample]
        event = self._getYEvent(x2, sample, client)
        ySample.append(event)
        return ySample

    def _defineYTest(self, sample, client, referenceDate):
        _, x2 = self.defineTrainWindowDates(referenceDate)
        yTest = []
        for date in range(x2 + 1, x2 + 1 + self.TEST_DAYS):
            event = self._getYEvent(date, sample, client)
            yTest.append(event)
        return yTest
    
    def _getYEvent(self, date, sample, client):
        xEvent = self._getXEvent(date, sample, client)
        return self._calculateYEventFromX(xEvent)
        
    def _calculateYEventFromX(self, xEvent):
        yEvent = [xEvent[0], xEvent[1] + xEvent[2], xEvent[3]]
        return yEvent 
        
    def _checkClient(self, sample, client):
        empty = len(sample[client]['x']) != 0
        return empty 

    def _encodeSample(self, cliente, xAmostra, yAmostra, yTest, lastX):
        amostraEncoded = {}
        amostraEncoded[cliente] = {}
        amostraEncoded[cliente]['x'] = xAmostra
        amostraEncoded[cliente]['y'] = yAmostra
        amostraEncoded[cliente]['ytest'] = yTest
        amostraEncoded[cliente]['lastX'] = lastX
        return amostraEncoded

    
###################################################################################################################    
# CLIP DATES
###################################################################################################################    

    def defineTrainWindowDates(self, referenceDate, window = 60):
        x2 = self._dateToNumber(referenceDate)
        x1 = x2 - window
        return [x1, x2]    

    def _dateToNumber(self, dateI):
        momento = dateI.split('/')
        dia = int(momento[0])
        mes = int(momento[1])
        ano = int(momento[2].split(' ')[0])
        return (datetime.datetime(ano, mes, dia) - self.__now).days    

