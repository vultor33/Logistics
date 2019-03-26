import collections
import json
import numpy as np
import re
import datetime

class CreateBatch: # trocar x por event
    def __init__(self):
        self.PRESENCA = 'Presen a'
        self.RUPTURA_LOJA = 'Ruptura em Loja'
        self.REPOSICAO = 'Reposi o'
        self.RUPTURA_GONDOLA = 'Ruptura em G ndola'
        self.DESCONHECIDO = 'Desconhecido'
        self.SEM_ESTOQUE = 'Sem Unidades Estocadas Armazenadas'
        self.COM_ESTOQUE = 'Unidades Estocadas Armazenadas'
        self.PRODUTO = 'Produto'
        self.OCORRENCIA1 = 'Ocorr ncia'
        self.OCORRENCIA2 = 'Ocorr ncia2'
        self.DATA_OCORRENCIA = 'dataDeOcorrencia'
        self.NOME_CLIENTE = 'Nome do cliente'
        self.TEST_DAYS = 7

###################################################################################################################    
# FILE HANDLING
###################################################################################################################    
        
    def exportBatch(self, batch, fileName = 'rupturaTable.json'):
        with open(fileName, 'w') as outfile:
            json.dump(batch, outfile)
    
    def loadBatch(self, fileName = 'rupturaTable.json'):
        with open('rupturaTable.json') as f:
            batchData = json.load(f)
        return batchData

###################################################################################################################    
# CREATE SAMPLES
###################################################################################################################    

    def create(self, data, itemName, referenceDate):
        itemIndexes = self.searchFlag(itemName, data, exactMatch = True)[itemName]
        data = data.loc[itemIndexes,:].copy()
        data = data.reset_index(drop=True)
        amostrasItem = self._convertToDict(data, itemName)
        amostras = self.applyOneHotEncoder(amostrasItem, referenceDate)
        return amostras
        #return self._applyOneHotEncoder(amostrasItem) refazer o oneHotEncoder

###################################################################################################################    
# SEARCH ITEM IN TABLES
###################################################################################################################    
        
    def searchFlag(self, flag, data, columnName = 'Produto', exactMatch = False):
        itemsFlag = {}
        for i in data.index:
            item = data.loc[i,columnName]
            itemEqual = self._itemIsEqual(item, flag, exactMatch)
            if itemEqual:
                if item not in itemsFlag:
                    itemsFlag[item] = [i]
                else:
                    itemsFlag[item].append(i)
        return itemsFlag

    def _itemIsEqual(self, item, flag, exactMatch):
        if exactMatch:
            return flag == item
        else:
            return flag in item

###################################################################################################################    
# TABLE TO DICTIONARY FORMAT
# - key = Nome do cliente-Produto
# - values
#          - x: ocorrencias  (presenca, ruptura, desconhecido e etc.)
#          - data: data da ocorrencia
###################################################################################################################    

    def _convertToDict(self, data, itemName):
        todosOsClientes = list(collections.Counter(data.loc[:,self.NOME_CLIENTE]))
        amostrasItem = {}
        for cliente in todosOsClientes:
            key = self._getKeyName(cliente, itemName)
            amostrasItem[key] = {}
            amostrasItem[key]['x'] = []
            amostrasItem[key]['data'] = []
        for i in data.index:
            cliente = data.loc[i,self.NOME_CLIENTE]
            key = self._getKeyName(cliente, itemName)
            dateI = data.loc[i,self.DATA_OCORRENCIA]
            ocorr = self._getRupturaType(data, i)
            amostrasItem[key]['x'].append(ocorr)
            amostrasItem[key]['data'].append(dateI)
        return amostrasItem

    def _getKeyName(self, cliente, itemName):
        cliente = re.sub('[^A-Za-z0-9]+', ' ', str(cliente))
        itemName = re.sub('[^A-Za-z0-9]+', ' ', str(itemName))
        return str(cliente) + '-' + str(itemName)

    def _getRupturaType(self, data, i):
        if data.loc[i,self.OCORRENCIA1] == self.REPOSICAO:
            if data.loc[i,self.OCORRENCIA2] == self.COM_ESTOQUE:
                return self.RUPTURA_GONDOLA
            else:
                return self.RUPTURA_LOJA
        else:
            return data.loc[i,self.OCORRENCIA1]    

###################################################################################################################    
# ENCODER
###################################################################################################################    
    
    def oneHotEncoder(self, element):
        if element == self.PRESENCA:
            return [1,0,0,0]
        elif element == self.RUPTURA_GONDOLA:
            return [0,1,0,0]
        elif element == self.RUPTURA_LOJA:
            return [0,0,1,0]
        elif element == self.DESCONHECIDO:
            return [0,0,0,1]
            
    def decriptEncoder(self, vector):
        if vector == [1,0,0,0]:
            return self.PRESENCA
        elif vector == [0,1,0,0]:
            return self.RUPTURA_GONDOLA
        elif vector == [0,0,1,0]:
            return self.RUPTURA_LOJA
        elif vector == [0,0,0,1]:
            return self.DESCONHECIDO
        
###################################################################################################################    
# APPLY ONE HOT ENCODER
###################################################################################################################    


    def applyOneHotEncoder(self, amostras, referenceDate):
        amostrasTodosClientes = {}
        for cliente in amostras:
            amostraEncoded = self._calculateAmostra(amostras, cliente, referenceDate)
            amostrasTodosClientes.update(amostraEncoded)
        return amostrasTodosClientes

    def _calculateAmostra(self, amostras, cliente, referenceDate):
        x1, x2 = self.defineTrainWindowDates(referenceDate)
        xAmostra = []
        for date in range(x1,x2):
            event = self._getEvent(date,amostras,cliente)
            xAmostra.append(event)
        yAmostra = list(xAmostra)
        yAmostra.pop(0)
        event = self._getEvent(x2,amostras,cliente)
        yAmostra.append(event)
        yTest = []
        for date in range(x2 + 2, x2 + 2 + self.TEST_DAYS):
            event = self._getEvent(date,amostras,cliente)
            yTest.append(event)
        amostraEncoded = self._encodeAmostra(cliente, xAmostra, yAmostra, yTest)
        return amostraEncoded

    def _getEvent(self, date, amostras, cliente):
        if date in amostras[cliente]['data']:
            dateIndex = amostras[cliente]['data'].index(date)
            event = amostras[cliente]['x'][dateIndex]
        else:
            event = self.DESCONHECIDO
        return self.oneHotEncoder(event)

    def _encodeAmostra(self, cliente, xAmostra, yAmostra, yTest):
        amostraEncoded = {}
        amostraEncoded[cliente] = {}
        amostraEncoded[cliente]['x'] = xAmostra
        amostraEncoded[cliente]['y'] = yAmostra
        amostraEncoded[cliente]['ytest'] = yTest
        return amostraEncoded

    
###################################################################################################################    
# CLIP DATES
###################################################################################################################    

    def defineTrainWindowDates(self, referenceDate, window = 60):
        y2 = self._dateToNumber(referenceDate)
        x2 = y2 - 1
        x1 = x2 - window
        return [x1, x2]    

    def _dateToNumber(self, dateI):
        momento = dateI.split('/')
        dia = int(momento[0])
        mes = int(momento[1])
        ano = int(momento[2].split(' ')[0])
        now = datetime.datetime.now()
        return (datetime.datetime(ano, mes, dia) - now).days    


        
######### APAGAR


    # NAO SEI SE AINDA E ADEQUADO
    def batch(self, amostras, nDiasTreino = 70, nDiasTeste = 10):
        nTotal = nDiasTreino + nDiasTeste
        Xtrain = []
        Ytrain = []
        Ytest = []
        for cliente in amostras:
            if self._checkAmostra(amostras[cliente]):
                continue
            if len(amostras[cliente]) > nTotal:
                xtrain = np.array(amostras[cliente][0:nDiasTreino])
                ytrain = np.array(amostras[cliente][1:nDiasTreino + 1])
                ytest = np.array(amostras[cliente][nDiasTreino:nTotal])
                Xtrain.append(xtrain)
                Ytrain.append(ytrain)
                Ytest.append(ytest)
        Xtrain = np.array(Xtrain)
        Ytrain = np.array(Ytrain)
        Ytest = np.array(Ytest)
        return [Xtrain,Ytrain,Ytest]

    def _checkAmostra(self, amostra):
        values = collections.Counter([str(x) for x in amostra])
        values = list(values.values())
        return len(values) <= 1

    
    
    
    
    def _applyOneHotEncoder(self, amostrasItem):
        for cliente in amostrasItem:
            datas = amostrasItem[cliente]['data']
            x = amostrasItem[cliente]['x']
            oneHot = []
            for i in range(max(datas) + 1):
                if i in datas:
                    iIndex = datas.index(i)
                    oneHot.append(self.oneHotEncoder(x[iIndex]))
                else:
                    oneHot.append(self.oneHotEncoder(self.DESCONHECIDO))
            amostrasItem[cliente] = oneHot
        return amostrasItem

        
        
        