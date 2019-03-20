import json
import pandas
import pickle
from core.util import cleanDataColumns
from core.util import generateScoreTable
from core.DataExploration import DataExploration
from core.FeatureTransform import FeatureTransform
from SmartCredit.ContratoConcatenating import ContratoConcatenating

class CrivoDeploy:
    def __init__(self, modelJson = 'SmartCredit1-4_mantenha_outliers.json', modelSav = 'smartcredit-1-4_model_COMPLETO.sav'):
        self.__MODEL_SAV_FILE = modelSav
        self.__MODEL_JSON_FILE = modelJson
        self.__NOK_FLAG = 'nok'
        self.__DIA_DE_CONCESSAO = ' Data'
        self.__COLUNA_CODIGO_PROPOSTA = 'Codigo proposta'
        self.__COLUNA_RECUSA_1 = 'BS Emprestimo Pessoal Carne Sistema '
        self.__COLUNA_RECUSA_2 = 'BS Emprestimo Pessoal Carne NC Sistema '

    def readCrivo(self, fileName):
         return pandas.read_csv(fileName,delimiter=';',encoding='latin-1',dtype=str)
        
    def removeDuplicates(self, data):  
        contCon = ContratoConcatenating()
        contCon.removeCrivoDuplicatesList(data)
        data = contCon.removeLines(data,contCon.PRE_REMOVE_FILE)
        data.index = range(len(data))
        return data
    
    def removeContratosRecusados(self,data):
        linesToDrop = []
        for i in data.index:
            if data.loc[i,self.__COLUNA_RECUSA_1] == self.__NOK_FLAG:
                linesToDrop.append(i)
            elif data.loc[i,self.__COLUNA_RECUSA_2] == self.__NOK_FLAG:
                linesToDrop.append(i)
        data = data.drop(linesToDrop)
        data.index = range(len(data))
        return data
    
    def cleanColumnNames(self, data):
        return cleanDataColumns(data)
    
    def aplicacaoDoJson(self, data):
        with open(self.__MODEL_JSON_FILE) as f:
            allOptions = json.load(f)
        featT = FeatureTransform()
        featT.setDateReference(data.loc[:,self.__DIA_DE_CONCESSAO])
        for colName in allOptions:
            data = featT.transform(data, colName,allOptions)
        data.index = range(len(data))
        codigoProposta = data.loc[:,self.__COLUNA_CODIGO_PROPOSTA].copy()
        columnNames = featT.getAllColumnsNames(allOptions)
        data = data.loc[:, columnNames]
        return data

    def generateScore(self, data):
        inadimpl = []
        for i in range(len(data)):
            inadimpl.append('0')        
        loaded_model = self.loadModel()
        dataScore = generateScoreTable(loaded_model,data,inadimpl)
        return dataScore
        
    def plotScore(self, dataScore):
        de = DataExploration(dataScore)
        de.setNpoints(9)
        de.setOutliersCut([None,None])
        de.graphicInadimplenciaXContinuum(dataScore, 'score')
        return dataScore

    def loadModel(self):
        return pickle.load(open(self.__MODEL_SAV_FILE, 'rb'))
     
    def plotScoreNoFormatoCrivoFred(self, fileName):
        dataTest = pandas.read_csv(fileName,delimiter=';',encoding='latin-1',dtype=str)
        dataTest = dataTest[dataTest.loc[:,'status'] == 'Aprovado']
        dataTest.index = range(len(dataTest))    
        inadimplentes = []
        score = []
        for i in range(len(dataTest)):
            score.append(int(dataTest.loc[i,'SCORE']))
            if dataTest.loc[i,'Inadimplente'] == 'Sim':
                inadimplentes.append('1')
            else:
                inadimplentes.append('0')
        score = pandas.DataFrame(data=score,columns = ['score'])
        inad = pandas.DataFrame(data=inadimplentes,columns = ['Inadimplente'])
        dataScore = pandas.concat([score,inad],axis=1)    
        de = DataExploration(dataScore)
        de.setNpoints(10)
        de.setOutliersCut([250,None])
        de.graphicInadimplenciaXContinuum(dataScore, 'score')
        
        
