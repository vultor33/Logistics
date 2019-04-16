import collections
import json
import numpy as np
import re
import datetime

from ruptura.TableToDictionary import TableToDictionary
from ruptura.Encoder import Encoder

class CreateBatch:
    def __init__(self, version):
        self.__version = version
        self.__tableToDictionary = TableToDictionary(version)
        self.__encoder = Encoder(version)
        self.titles = []

    def batch(self, fileName, sampleShape = (60,4)):
        amostras = self.loadBatch(fileName)
        print('WARNING - need error handling on samples')
        X = []
        Y = []
        Ytest = []
        for key in amostras:
            x = np.array(amostras[key]['x'])
            y = np.array(amostras[key]['y'])
            yt = np.array(amostras[key]['ytest'])
            if x.shape != sampleShape:
                continue
            X.append(x)
            Y.append(y)
            Ytest.append(yt)
            self.titles.append(key)
        X = np.array(X)
        Y = np.array(Y)
        Ytest = np.array(Ytest)
        return[X, Y, Ytest]

###################################################################################################################    
# FILE HANDLING
###################################################################################################################    
        
    def exportBatch(self, batch, fileName = 'rupturaTable.json'):
        with open(fileName, 'w') as outfile:
            json.dump(batch, outfile)
    
    def loadBatch(self, fileName = 'rupturaTable.json'):
        with open(fileName) as f:
            batchData = json.load(f)
        return batchData

###################################################################################################################    
# CREATE SAMPLES
###################################################################################################################    

    def create(self, data, word, referenceDate):
        allProds = self._searchAllProducts(word, data)
        allSamples = {}
        for prod in allProds:
            sample = self.createItem(data, prod, referenceDate)
            allSamples.update(dict(sample))
        return allSamples

    def createItem(self, data, itemName, referenceDate):
        itemIndexes = self.searchFlag(itemName, data, exactMatch = True)[itemName]
        data = data.loc[itemIndexes,:].copy()
        data = data.reset_index(drop=True)
        #return self.__tableToDictionary.convertToDict(data, itemName)
        amostrasItem = self.__tableToDictionary.convertToDict(data, itemName) #continuando
        amostras = self.__encoder.applyOneHotEncoder(amostrasItem, referenceDate)
        return amostras

###################################################################################################################    
# SEARCH ITEM IN TABLES
###################################################################################################################    

    def _searchAllProducts(self, word, data):
        products = list(collections.Counter(data.loc[:,self.PRODUTO]))
        allProd  = []
        for prod in products:
            if word in prod:
                allProd.append(prod)
        return allProd
        
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
