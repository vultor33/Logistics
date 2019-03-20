import pandas
from core.util import removeSpecialCharacters

class VariablesCorrelation:

    def __init__(self, targetCol):
        """
        Example:
        varCorr = VariablesCorrelation(targetCol)
        varCorr.correlationBetweenColumns(alldata)    
        """
        self.__THRESHOULD = 0.99
        self.columnCorrelatedFileName = 'PearsonColumnsCorrelated.csv'
        self.columnTargetCorrelatedFileName = 'PearsonColumnsTargetCorrelated.csv'
        self.__targetCol = targetCol
        self.__notCorrelatedColumns = []
    
    def correlationBetweenColumns(self, alldata):
        data = alldata.drop(self.__targetCol, axis=1)
        corr = data.corr()
        columns = corr.columns
        fullCorrelations = {}
        alreadyCorrelated = []
        for colI in corr.columns:
            if colI in alreadyCorrelated:
                continue
            fullCorrelations[colI] = []
            for colJ in corr.loc[:,colI].index:
                if colI == colJ:
                    continue
                if abs(corr.loc[colI,colJ]) > self.__THRESHOULD:
                    fullCorrelations[colI].append(colJ)
                    alreadyCorrelated.append(colJ)
        self._printColumnsCorrelations(fullCorrelations)
        self.__notCorrelatedColumns = list(fullCorrelations.keys())
        self.__notCorrelatedColumns.append('Inadimplente')
        self._correlationWithTargetColumns(alldata, self.__notCorrelatedColumns)

    def printTargetCorrelations(self):
        trueInadCorr = pandas.read_csv(self.columnTargetCorrelatedFileName,delimiter=';',encoding='latin-1')
        for col in trueInadCorr.columns:
            if abs(trueInadCorr.loc[0,col]) > (1-self.__THRESHOULD):
                print(round(trueInadCorr.loc[0,col],2),'   ',col)

    def getNotCorrelatedColumns(self):
        return self.__notCorrelatedColumns
        
    def _printColumnsCorrelations(self, fullCorrelations):
        file = open(self.columnCorrelatedFileName,'w')
        for col in fullCorrelations:
            if len(fullCorrelations[col]) > 0:
                file.write(removeSpecialCharacters(col) + ';')
                for colI in fullCorrelations[col]:
                    file.write(removeSpecialCharacters(colI) + ';')
                file.write('\n')
        file.close()
        
    def _correlationWithTargetColumns(self, alldata, columns):
        file = open(self.columnTargetCorrelatedFileName, 'w')
        for col in columns:
            file.write(removeSpecialCharacters(col) + ';')
        file.write('\n')
        for col in columns:
            notNanData = alldata[alldata.loc[:,col] != alldata.loc[:,col].min()].copy()
            corCol = notNanData.corr()
            file.write(str(corCol.loc[self.__targetCol,col]) + ';')
        file.write('\n')
        file.close()
            