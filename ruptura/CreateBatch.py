import collections
import json
import numpy as np
import re

class CreateBatch:
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
   
    def create(self, data, itemName):
        itemIndexes = self.searchFlag(itemName, data, exactMatch = True)[itemName]
        data = self._calculateData(data, itemIndexes)
        amostrasItem = self._convertToDict(data, itemName)
        return self._applyOneHotEncoder(amostrasItem)
      
    def exportBatch(self, batch, fileName = 'rupturaTable.json'):
        with open(fileName, 'w') as outfile:
            json.dump(batch, outfile)
    
    def loadBatch(self, fileName = 'rupturaTable.json'):
        with open('rupturaTable.json') as f:
            batchData = json.load(f)
        return batchData
        
    def _calculateData(self, data, index):
        data = data.loc[index,:].copy()
        data = data.reset_index(drop=True)
        minData = min(data.loc[:,self.DATA_OCORRENCIA])
        data.loc[:,self.DATA_OCORRENCIA] = data.loc[:,self.DATA_OCORRENCIA] - minData #regularizacao das datas        
        return data

    def _convertToDict(self, data, itemName):
        todosOsClientes = list(collections.Counter(data.loc[:,self.NOME_CLIENTE]))
        amostrasItem = {}
        for cliente in todosOsClientes:
            key = str(cliente) + '-' + str(itemName)
            key = re.sub('[^A-Za-z0-9]+', ' ', str(key))
            amostrasItem[key] = {}
            amostrasItem[key]['x'] = []
            amostrasItem[key]['data'] = []
        for i in data.index:
            cliente = data.loc[i,self.NOME_CLIENTE]
            key = str(cliente) + '-' + str(itemName)
            key = re.sub('[^A-Za-z0-9]+', ' ', str(key))
            dateI = data.loc[i,self.DATA_OCORRENCIA]
            ocorr = self._getRupturaType(data, i)
            amostrasItem[key]['x'].append(ocorr)
            amostrasItem[key]['data'].append(dateI)
        return amostrasItem

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

    def _getRupturaType(self, data, i):
        if data.loc[i,self.OCORRENCIA1] == self.REPOSICAO:
            if data.loc[i,self.OCORRENCIA2] == self.COM_ESTOQUE:
                return self.RUPTURA_GONDOLA
            else:
                return self.RUPTURA_LOJA
        else:
            return data.loc[i,self.OCORRENCIA1]    

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

    def _checkAmostra(self, amostra):
        values = collections.Counter([str(x) for x in amostra])
        values = list(values.values())
        return len(values) <= 1
        
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
        
        