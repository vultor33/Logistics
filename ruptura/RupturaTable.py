import re
import datetime
import pandas as pd

class RupturaTable:
    def __init__(self):
        self.PRODUTO = 'Produto'
        self.OCORRENCIA1 = 'Ocorr ncia'
        self.OCORRENCIA2 = 'Ocorr ncia2'
        self.DATA_OCORRENCIA = 'dataDeOcorrencia'
        self.DATA_ENCERRAMENTO_OS = 'Data Hora de encerramento da OS'
        self.DIA_SEMANA = 'DiaDaSemana'
        
        self.__now = datetime.datetime.now()
        self.__data = []
    
    def generate(self, files, clipData):
        self.loadFiles(files)
        self.removeOutliers()
        self.cleanData()
        self.convertDataFormat()
        self.clipDates(clipData[0], clipData[1])
    
    def getData(self):
        return self.__data
    
    def loadFiles(self, files):
        allData = []
        for file in files:
            dataI = pd.read_csv(file,delimiter=';',encoding='latin-1',dtype=str)
            allData.append(dataI)
        self.__data = pd.concat(allData,ignore_index=True)

    def removeOutliers(self):
        self.__data = self.dropNan(self.__data, self.OCORRENCIA1)
        self.__data = self.dropNan(self.__data, self.OCORRENCIA2)
        self.__data = self.dropNan(self.__data, self.PRODUTO)
        self.__data = self.dropNan(self.__data, self.DATA_ENCERRAMENTO_OS)        

    def dropNan(self, data, columnName):
        indexNan = data[data.loc[:,columnName].isnull()].index
        data = data.drop(indexNan)
        data = data.reset_index(drop=True)
        return data
    
    def convertDataFormat(self):
        allDates = []
        weekDays = []
        for i in self.__data.index:
            dateI = self.__data.loc[i,self.DATA_ENCERRAMENTO_OS]
            weekDay = self.datetimeFromStringDate(dateI).weekday()
            weekDays.append(weekDay)
            dateI = int(self.daysFromNowConvertDate(dateI))
            allDates.append(dateI)
        self.__data[self.DATA_OCORRENCIA] = allDates    
        self.__data[self.DIA_SEMANA] = weekDays
        
    def daysFromNowConvertDate(self, dateI):
        dateI = self.datetimeFromStringDate(dateI)
        return (dateI - self.__now).days    

    def datetimeFromStringDate(self, dateI):
        momento = dateI.split('/')
        dia = int(momento[0])
        mes = int(momento[1])
        ano = int(momento[2].split(' ')[0])
        return datetime.datetime(ano, mes, dia)
    

    def clipDates(self, start, end):
        start = self.daysFromNowConvertDate(start)
        end = self.daysFromNowConvertDate(end)
        startDropIndex = self.__data[self.__data.loc[:,self.DATA_OCORRENCIA].values < start].index
        self.__data = self.__data.drop(startDropIndex)
        self.__data = self.__data.reset_index(drop=True)
        endDropIndex = self.__data[self.__data.loc[:,self.DATA_OCORRENCIA].values > end].index
        self.__data = self.__data.drop(endDropIndex)
        self.__data = self.__data.reset_index(drop=True)

    def cleanData(self):
        self.cleanDataColumns()
        self.cleanOcorrenciaColumns()
        
    def cleanDataColumns(self):
        trueCol = []
        for col in self.__data.columns:
            trueCol.append(self.removeSpecialCharacters(col))
        self.__data.columns = trueCol        
 
    def cleanOcorrenciaColumns(self):
        ocorr1 = list(self.__data.loc[:,self.OCORRENCIA1])
        self.__data.loc[:,self.OCORRENCIA1] = [self.removeSpecialCharacters(x) for x in ocorr1]
        ocorr2 = list(self.__data.loc[:,self.OCORRENCIA2])
        self.__data.loc[:,self.OCORRENCIA2] = [self.removeSpecialCharacters(x) for x in ocorr2]

    def removeSpecialCharacters(self, value):
        return re.sub('[^A-Za-z0-9]+', ' ', str(value))

