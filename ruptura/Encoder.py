import datetime
from ruptura.EncoderX import EncoderX
from ruptura.EncoderY import EncoderY

class Encoder:
    def __init__(self, version):
        self.TEST_DAYS = 7
        self.__version = version
        self.__now = datetime.datetime.now()
        self.__encoderX = EncoderX(version)
        self.__encoderY = EncoderY(version)

    def applyOneHotEncoder(self, sample, referenceDate):
        allSamples = {}
        for client in sample:
            if not self._checkClient(sample, client):
                continue
            xSample, lastX = self._defineX(sample[client], referenceDate)      # try sample[client]
            ySample, yTest = self._defineY(sample[client], referenceDate)
            encodedSample = self._encodeSample(client, xSample, ySample, yTest, lastX)
            allSamples.update(encodedSample)
        return allSamples

    def getUnknwows(self):
        return [self.__encoderX.getXUnknwow(), self.__encoderY.getYUnknwow()]

    def _defineX(self, sample, referenceDate):
        x1, x2 = self.defineTrainWindowDates(referenceDate)
        xSample = []
        for date in range(x1,x2):
            event = self.__encoderX.calculateXEvent(date, sample)
            xSample.append(event)
        lastX = self.__encoderX.calculateXEvent(x2, sample)
        return [xSample, lastX]

    def _defineY(self, sample, referenceDate):
        x1, x2 = self.defineTrainWindowDates(referenceDate)
        ySample = []
        for date in range(x1 + 1, x2 + 1):
            event = self.__encoderY.calculateYEvent(date, sample)
            ySample.append(event)
        yTest = []
        for date in range(x2 + 1, x2 + 1 + self.TEST_DAYS):
            event = self.__encoderY.calculateYEvent(date, sample)
            yTest.append(event)
        return ySample, yTest
        
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




