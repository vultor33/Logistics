

class EncoderX:
    """ Transform data into one hot encoder format for X variable """
    def __init__(self,version):
        self.__version = version
        self.__UNKNWOW = self._generateUnknow()
        self._defineConstants()
        
    def calculateXEvent(self, xDate, sample):
        if xDate in sample['data']:
            dateIndex = sample['data'].index(xDate)
            event = self._generateX(sample['x'][dateIndex])
        else:
            event = self.__UNKNWOW
        return event        

    def getXUnknwow(self):
        return self.__UNKNWOW
    
################################################################################################    
# GENERATE X
################################################################################################

    def _generateX(self, xDict):
        if self.__version[0:4] == '0-1-':
            return self._generateXv01(xDict)
        else:
            raise Exception('Version ' + self.__version + ' not implemented in EncoderX')
        
    def _generateXv01(self, xDict):
        ocorr1 = xDict[self.OCORRENCIA1]
        ocorr2 = xDict[self.OCORRENCIA2]
        if ocorr1 == self.RUPTURA_GONDOLA or ocorr1 == self.RUPTURA_GONDOLA:
            xOcorr = 0
        elif ocorr1 == self.REPOSICAO:
            xOcorr = 0.33
        else:
            xOcorr = 1
        if ocorr2 == self.COM_ESTOQUE:
            xEstoque = 1
        else:
            xEstoque = 0
        return [xOcorr, xEstoque, 0]        
    
################################################################################################    
# GENERATE UNKNOW
################################################################################################

    def _generateUnknow(self):
        if self.__version[0:4] == '0-1-':
            return self._generateUnknowXv01()
        else:
            raise Exception('Version ' + self.__version + ' not implemented in EncoderX')

    def _generateUnknowXv01(self):
        return [0,0,1]
        
################################################################################################    
# DEFINE CONSTANTS
################################################################################################
    
    def _defineConstants(self):
        if self.__version[0:4] == '0-1-':
            return self._defineConstantsXv01()
        else:
            raise Exception('Version ' + self.__version + ' not implemented in EncoderX')
        
    def _defineConstantsXv01(self):
        self.OCORRENCIA1 = 'Ocorr ncia'
        self.OCORRENCIA2 = 'Ocorr ncia2'
        self.RUPTURA_GONDOLA = 'Ruptura em G ndola'
        self.REPOSICAO = 'Reposi o'
        self.COM_ESTOQUE = 'Unidades Estocadas Armazenadas'
        
        
        