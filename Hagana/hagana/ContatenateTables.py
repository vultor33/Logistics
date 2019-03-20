import pandas
import datetime
import numpy

class ContatenateTables:
    def __init__(self, fileInspecoes, fileRecisoes):
        self.dataInspecoes = pandas.read_excel(fileInspecoes,delimiter=';',encoding='latin-1',dtype=str)
        dataRecis = pandas.read_csv(fileRecisoes,delimiter=';',encoding='latin-1',dtype=str)
        self.__codigoRecisoes = list(dataRecis.loc[:,'Codigo do Posto'])
        self.__codigosAdded = []

    def getCodigosRecisao(self):
        return self.__codigosAdded

    def generateRecisaoColStatus(self):
        recisaoCol = []
        for i in self.dataInspecoes.index:
            codigo = self.dataInspecoes.loc[i,'codigo']
            if codigo in self.__codigosAdded:
                recisaoCol.append('1')
            elif codigo in self.__codigoRecisoes:
                recisaoCol.append('1')
                self.__codigosAdded.append(codigo)
            else:
                recisaoCol.append('0')
        self.dataInspecoes['recisaoCol'] = recisaoCol
    
    def getCodigosRecisoesNotFound(self):
        codeNotFound = []
        for code in self.__codigoRecisoes:
            if code not in self.__codigosAdded:
                codeNotFound.append(code)
        return codeNotFound

    def takeOnlyNumberFromGrade(self, data):
        colNota = ['supervisao','grupo', 'diurna', 'noturna', 'equipamentos']
        for col in colNota:
            colNotaModified = []
            for i in data.index:
                notaI = str(data.loc[i,col])
                if notaI == 'nan':
                    colNotaModified.append(-1)
                else:
                    colNotaModified.append(int(notaI.split(' ')[0]))
            data[col] = colNotaModified
        return data

    def transformTimeUnit(self, data):
        zeroTime = datetime.datetime(2000,1,1)
        dataCol = 'data'
        dataModified = []
        for i in data.index:
            dataI = str(data.loc[i,dataCol])
            if dataI == 'nan':
                dataModified.append(numpy.nan)
            else:
                dataIsplit1 = dataI.split('-')
                year = int(dataIsplit1[0])
                month = int(dataIsplit1[1])
                day = int(dataIsplit1[2].split(' ')[0])
                tempoI = datetime.datetime(year,month,day)
                diffTime = (tempoI - zeroTime).days
                dataModified.append(diffTime)
        data[dataCol] = dataModified
        return data
