###################################################################################################################    
# TABLE TO DICTIONARY FORMAT
# - key = Nome do cliente-Produto
# - values
#          - x: vetor com infromacoes das medidas referentes naquele dia [presenca, ruptura, e etc.]
#          - data: data da ocorrencia
###################################################################################################################    

import re
import collections

class TableToDictionary:
    def __init__(self, version):
        self._defineTableNames()
        self.__version = version

    def convertToDict(self, data, itemName):
        sampleItem = self._defineSample(data, itemName)
        sampleItem = self._createSampleItem(data, itemName, sampleItem)
        return sampleItem

    def _createSampleItem(self, data, itemName, sampleItem):
        for i in data.index:
            key = self._getKey(data, i, itemName)
            dateI = data.loc[i,self.DATA_OCORRENCIA]
            xValue = self._extractAllRelevantInformation(data, i)
            self._addToSample(sampleItem, key, dateI, xValue)
        return sampleItem
    
    def _addToSample(self, sampleItem, key, dateI, xValue):
        sampleItem[key]['x'].append(xValue)
        sampleItem[key]['data'].append(dateI)
    
    def _getKey(self, data, i, itemName):
        client = data.loc[i,self.NOME_CLIENTE]
        return self._getKeyName(client, itemName)
        
    def _getKeyName(self, client, itemName):
        client = re.sub('[^A-Za-z0-9]+', ' ', str(client))
        itemName = re.sub('[^A-Za-z0-9]+', ' ', str(itemName))
        return str(client) + '-' + str(itemName)

    def _extractAllRelevantInformation(self, data, i):
        x = {}
        x[self.OCORRENCIA1] = data.loc[i,self.OCORRENCIA1]
        x[self.OCORRENCIA2] = data.loc[i,self.OCORRENCIA2]
        x[self.DIA_MES_ANO] = data.loc[i,self.DIA_MES_ANO]
        return x

    def _defineSample(self, data, itemName):
        allClients = list(collections.Counter(data.loc[:,self.NOME_CLIENTE]))
        sampleItem = {}
        for client in allClients:
            key = self._getKeyName(client, itemName)
            sampleItem[key] = {}
            sampleItem[key]['x'] = []
            sampleItem[key]['data'] = []
        return sampleItem
        
    def _defineTableNames(self):
        self.NOME_CLIENTE = 'Nome do cliente'
        self.OCORRENCIA1 = 'Ocorr ncia'
        self.OCORRENCIA2 = 'Ocorr ncia2'
        self.DATA_OCORRENCIA = 'dataDeOcorrencia'
        self.PRESENCA = 'Presen a'
        self.RUPTURA_LOJA = 'Ruptura em Loja'
        self.REPOSICAO = 'Reposi o'
        self.RUPTURA_GONDOLA = 'Ruptura em G ndola'
        self.DESCONHECIDO = 'Desconhecido'
        self.SEM_ESTOQUE = 'Sem Unidades Estocadas Armazenadas'
        self.COM_ESTOQUE = 'Unidades Estocadas Armazenadas'
        self.PRODUTO = 'Produto'
        self.DIA_SEMANA = 'DiaDaSemana'
        self.DIA_MES_ANO = 'Data Hora de encerramento da OS'

    
    
        
        