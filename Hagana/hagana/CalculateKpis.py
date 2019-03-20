import matplotlib.pyplot as plt
import collections

class CalculateKpis:
    def __init__(self, data):
        self.__data = data
        self.__allColOptions = self._calculateAllOptions()

    def kpiOfCodes(self, recisaoCodes):
        stats = self._statsOfCodes(recisaoCodes)
        nSamples = len(recisaoCodes)
        return self._calculateMeanOfStats(stats, nSamples)
        
    def plotAllGraphics(self, meanOfStatsRecisao,meanOfStatsSemRecis):    
        for colName in meanOfStatsRecisao:
            for option in meanOfStatsRecisao[colName]:
                optionRecisao = meanOfStatsRecisao[colName][option]
                optionAtivo = meanOfStatsSemRecis[colName][option]
                if option == '-1':
                    option = 'NULO'
                if option == '1':
                    option = 'PESSIMO'
                if option == '2':
                    option = 'RUIM'
                if option == '3':
                    option = 'REGULAR'
                if option == '4':
                    option = 'BOM'
                if option == '5':
                    option = 'OTIMO'
                if option == '6':
                    option = 'NAO SE APLICA'
                self._plotRecisaoGraph(colName + '(' + option + ')',optionRecisao,optionAtivo)
                
    def _calculateAllOptions(self):
        self.__allColKpi = ['supervisao',
                     'grupo', 
                     'diurna', 
                     'noturna', 
                     'equipamentos', 
                     'indicaria', 
                     'sugestao',
                     'area', 
                     'falta', 
                     'cargo']
        allColOptions = {}
        for colName in self.__allColKpi:
            allColOptions[colName] = list(collections.Counter(self.__data.loc[:,colName]).keys())
        return allColOptions

    def _calculateStats(self, colName, code):
        colOptions = self.__allColOptions[colName]
        dataCode = self.__data[self.__data.loc[:,'codigo'] == code].copy()
        nSamples = len(dataCode)
        if nSamples == 0:
            return {}

        dataCodeStats = collections.Counter(dataCode.loc[:,colName])
        for option in colOptions:
            if option not in dataCodeStats:
                dataCodeStats[option] = 0
            else:
                dataCodeStats[option] = dataCodeStats[option] / nSamples
        return dataCodeStats


    def _statsOfCodes(self, listOfCodes):
        statsOfCodes = {}
        for code in listOfCodes:
            statsOfCodes[code] = {}
            for colName in self.__allColKpi:
                statsOfCodes[code][colName] = self._calculateStats(colName, code)
        return statsOfCodes
    
    def _calculateMeanOfStats(self, stats, nSamples):
        statsMean = {}
        for colName in self.__allColOptions:
            statsMean[colName] = {}
            for option in self.__allColOptions[colName]:
                statsMean[colName][option] = 0
    
        for code in stats:
            for colName in stats[code]:
                for option in stats[code][colName]:
                    statsMean[colName][option] += stats[code][colName][option]
            
        for colName in self.__allColOptions:
            for option in self.__allColOptions[colName]:
                statsMean[colName][option] = statsMean[colName][option]/nSamples
        
        return statsMean           

    def _plotRecisaoGraph(self, indicador, recKpi, ativoKpi):
        fig, ax = plt.subplots()
        ax.set_ylabel('Quantidade em contratos (%)')
        ax.set_title(indicador)
        ax.set_xticks([0,1])
        ax.set_xticklabels(('RECISAO', 'ATIVO'))
        ax.bar([0,1], [recKpi,ativoKpi], color=((1,0,0),(0,0,1)))
        fig.savefig(indicador + '-kpi.png', dpi=150)
        del fig
        del ax

