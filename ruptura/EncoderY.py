

class EncoderY:
    """ Transform data into one hot encoder format for Y variable """
    def __init__(self,version):
        self.REPOSICAO_VALUE = 0.33
        self.__version = version
        self.__UNKNWOW = self._generateUnknow()
        self._defineConstants()
        
    def calculateYEvent(self, xDate, sample):
        print('DEPRECATED - should be removed in future version')
        if xDate in sample['data']:
            dateIndex = sample['data'].index(xDate)
            event = self._generateY(sample['x'][dateIndex])
        else:
            event = self.__UNKNWOW
        return event        

    def getYUnknwow(self):
        return self.__UNKNWOW
    
################################################################################################    
# GENERATE Y
################################################################################################

    def _generateY(self, xDict):
        if self.__version[0:4] == '0-1-':
            return self._generateYv01(xDict)
        else:
            raise Exception('Version ' + self.__version + ' not implemented in EncoderY')
        
    def _generateYv01(self, xDict):
        ocorr1 = xDict[self.OCORRENCIA1]
        if ocorr1 == self.RUPTURA_GONDOLA or ocorr1 == self.RUPTURA_LOJA:
            yOcorr = 0
        elif ocorr1 == self.REPOSICAO:
            yOcorr = self.REPOSICAO_VALUE
        elif ocorr1 == self.PRESENCA:
            yOcorr = 1
        else:
            raise Exception('ocorrencia nao definida:  ' + str(ocorr1))
        return [yOcorr, 0]        
    
################################################################################################    
# GENERATE UNKNOW
################################################################################################

    def _generateUnknow(self):
        if self.__version[0:4] == '0-1-':
            return self._generateUnknowYv01()
        else:
            raise Exception('Version ' + self.__version + ' not implemented in EncoderY')

    def _generateUnknowYv01(self):
        return [0,1]
        
################################################################################################    
# DEFINE CONSTANTS
################################################################################################
    
    def _defineConstants(self):
        if self.__version[0:4] == '0-1-':
            return self._defineConstantsYv01()
        else:
            raise Exception('Version ' + self.__version + ' not implemented in EncoderY')
        
    def _defineConstantsYv01(self):
        self.OCORRENCIA1 = 'Ocorr ncia'
        self.RUPTURA_GONDOLA = 'Ruptura em G ndola'
        self.RUPTURA_LOJA = 'Ruptura em Loja'
        self.REPOSICAO = 'Reposi o'
        self.PRESENCA = 'Presen a'
        self.COM_ESTOQUE = 'Unidades Estocadas Armazenadas'
        