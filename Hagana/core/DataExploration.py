import pandas
import seaborn
import matplotlib.pyplot as plt
import collections
import numpy
from sklearn import metrics
from core.MachineLearningOptions import MachineLearningOptions
from core.util import removeOutliersWithLimits, breakColIntoAdimAndInad

class DataExploration:

    def __init__(self, data = []):
        """ Tool to collect data plots\n
        WARNING: check categoryPercentage for implementation\n
        Input\n
        obj: MachineLearningOptions
        Output\n
        plotAllGraphics gives some graphics for Credit Score\n
        scatterColumns just save the scatter\n
        plotMeasureVsPredicted plot measure vs predicted and plot it with R2\n
        """
        self.__CORRELATION_GRAPHIC = '-CORRELATION'
        self.__PERCENTAGE_GRAPHIC = '-PERCENTAGE'
        self.__CATEGORY_GRAPHIC = '-CATEGORY'
        self.__NUMBER_GRAPHIC = '-NUMBER'
        self.__CORRELATION_GRAPHIC = 'CorrelationGraphic'
        self.__DATA_FORMAT = '.png'
        self.__COUNT_AXIS = 'Count'
        self.__N_POINTS = 20
        self.__OUTLIERS_CUT = [None, None]
        self.__FONT_SIZE = 12
        self.__customCategoryTypes = []
        self._setData(data)

    def _setData(self, data):
        if len(data) != 0:
            mlOptions = MachineLearningOptions()
            mlOptions.data = data
            self.setMachineLearningOptions(mlOptions)

    def setMachineLearningOptions(self, machineLearningOptions):
        self.__data = machineLearningOptions.data
        self.__names = list(self.__data)
        self.__columnY = machineLearningOptions.targetColumn
        self.__targetPercentage = machineLearningOptions.getTargetPercentagePlot()
        self.__isToCorrelateWithTargetColumn = machineLearningOptions.getTargetColumnIsNumber()

    def findCorrelation(self, data, threshold = 0.9, remove_negative = False):
        corr_mat = data.corr()
        if remove_negative:
            corr_mat = numpy.abs(corr_mat)
        corr_mat = numpy.tril(corr_mat, k=-1)
        already_in = set()
        perfect_corr = []
        for i in range(len(corr_mat)):
            for j in range(len(corr_mat[i])):
                if corr_mat[i][j] > threshold:
                    perfect_corr.append([i,j])
                    break
        return perfect_corr

    def plotAllGraphics(self):
        varTypes = self.__data.dtypes
        self._correlationHeatMap()
        for i in range(len(varTypes)):
            if varTypes[i] == object:
                if i != self.__columnY:
                    self._categoryPercentage(i,self.__columnY)
                    self._countCategoryFile(i)
                else:
                    self._countPlotFigure(i)
            elif varTypes[i] != object:
                self._histogramPlotFigure(i)

    def scatterColumns(self, columnX, columnY, labels = []):
        fig, ax = plt.subplots()
        ax.scatter(columnX,columnY, edgecolors=(0, 0, 0))
        if len(labels) > 0:
            ax.set_title(labels[0])
            ax.set_xlabel(labels[1])
            ax.set_ylabel(labels[2])
            fig.savefig(labels[0] + '-scatter' +  self.__DATA_FORMAT, dpi=150)
        else:
            fig.savefig('scatter' + self.__DATA_FORMAT, dpi=150)
        plt.close(fig)        

    def plotMeasureVsPredicted(self, measured, predicted, labels = []):
        R2 = metrics.r2_score(measured,predicted)
        fig, ax = plt.subplots()
        ax.scatter(measured, predicted, edgecolors=(0, 0, 0))
        ax.plot(
                [numpy.min(measured), numpy.max(measured)], 
                [numpy.min(measured), numpy.max(measured)], 'k', lw=4)
        up = max(predicted) * 1.1
        down = min(predicted) * 0.9
        xMin = min(measured)
        ax.set_ylim(down, up)
        ax.annotate('R2=' + "%.2f" % R2, xy=(xMin, up + (down - up) * 0.1), fontsize=20)
        if len(labels) > 0:
            ax.set_title(labels[0])
            ax.set_xlabel(labels[1])
            ax.set_ylabel(labels[2])
            fig.savefig(labels[0] + '-measuredVspredicted' + self.__DATA_FORMAT, dpi=150)
        else:
            ax.set_xlabel('Measured')
            ax.set_ylabel('Predicted')
            fig.savefig('measuredVspredicted' + self.__DATA_FORMAT, dpi=150)
        plt.close(fig)        
        
    def setCustomCategoryTypes(self, catTypes):
        self.__customCategoryTypes = catTypes

#FOR CATEGORIES
    def _countPlotFigure(self, column):
        orderCat = self._calculateCategoryTypes(column).keys()
        seaPlot = seaborn.countplot(x=self.__names[column], data=self.__data, order=orderCat)
        fig = seaPlot.get_figure()
        fig.savefig(self.__names[column] + self.__CATEGORY_GRAPHIC + self.__DATA_FORMAT, dpi=150)
        plt.close(fig)

    def _countCategoryFile(self, column):
        countCategory = self._calculateCategoryTypes(column)
        file = open('count-' + self.__names[column] + '.csv', 'w')
        for feature in countCategory:
            if self._isNan(feature):
                file.write(str(feature) + ';' + str(countCategory[feature]) + '\n')
            else:
                file.write(str(feature.encode("utf-8")) + ';' + str(countCategory[feature]) + '\n')
        file.close()

    def _categoryPercentage(self, column, COLUMN_Y):
        catChar = self._calculateCategoryProperties(column, COLUMN_Y)
        fig = plt.figure()
        self._annotatePercentages(fig,catChar)
        self._twoBarsPlot(fig,catChar,column)

    def _calculateCategoryProperties(self,column, COLUMN_Y):
        catChar = CategoryCharacteristics()
        allDefaults = self.__data.loc[self.__data[self.__names[COLUMN_Y]] == self.__targetPercentage]
        if self.__customCategoryTypes != []:
            categoryTypes = self.__customCategoryTypes
        else:
            categoryTypes = self._calculateCategoryTypes(column).keys()
        for cat in categoryTypes:
            nDefault = self._calculateNumberOfOccurrences(allDefaults,column,cat)
            nTotal = self._calculateNumberOfOccurrences(self.__data, column, cat)
            catChar.addValues(cat, nDefault, nTotal)
        return catChar

    def _calculateCategoryTypes(self, column):
        category = self.__data.iloc[:,column].copy()
        categoryTypes = collections.Counter(category)
        return categoryTypes

    def _annotatePercentages(self, fig, catChar):
        totalHeight = catChar.getTotalCount()
        labels = catChar.getAllLabels()
        allPercentages = catChar.getAllPercentages()
        ax = fig.add_subplot(111)
        up = max(totalHeight) * .05
        ax.set_ylim(0, max(totalHeight) + 3 * up)
        y_pos = numpy.arange(len(labels))
        for xi, yi, l in zip(*[y_pos, totalHeight, list(map(str, allPercentages))]):
            ax.text(xi - len(l) * .05, yi + up, l, bbox=dict(facecolor='w', edgecolor='w', alpha=.5))

    def _twoBarsPlot(self,fig, catChar, column):
        allCatDefaultNumbers = catChar.getAllCatDefaultNumbers()
        allCatNonDefaultNumbers = catChar.getAllCatNonDefaultNumbers()
        labels = catChar.getAllLabels()
        y_pos = numpy.arange(len(labels))
        plt.bar(y_pos, allCatDefaultNumbers, color= 'r')
        plt.bar(y_pos, allCatNonDefaultNumbers, bottom=allCatDefaultNumbers, color='b')
        plt.xticks(y_pos, labels)
        plt.xlabel(self.__names[column])
        plt.ylabel(self.__COUNT_AXIS)
        fig.savefig(self.__names[column] + self.__PERCENTAGE_GRAPHIC + self.__DATA_FORMAT, dpi=150)

    def _calculateNumberOfOccurrences(self, data, column, feature):
        if self._isNan(feature):
            col = data.iloc[:,column]
            return col.isnull().sum()
        else:
            colCount = data.loc[data[self.__names[column]] == feature]
            return len(colCount)
        

    def _isNan(self, value):
        if isinstance(value, str):
            return False
        elif numpy.isnan(value):
            return True
        else:
            return False

#FOR NUMBERS
    def _histogramPlotFigure(self, column):                
        seaPlotNumber = seaborn.distplot(self.__data.loc[:,self.__names[column]])
        figNumber = seaPlotNumber.get_figure()
        figNumber.savefig(self.__names[column] + self.__NUMBER_GRAPHIC + self.__DATA_FORMAT, dpi=150)
        plt.close(figNumber)

    def _boxPlotFigure(self, column):    
        """ DEPRECATED - will be removed on future versions """
        seaPlotNumber = seaborn.boxplot(
                y=self.__names[column],
                data=self.__data)
        figNumber = seaPlotNumber.get_figure()
        figNumber.savefig(self.__names[column] + self.__NUMBER_GRAPHIC + self.__DATA_FORMAT, dpi=150)
        plt.close(figNumber)

    def _correlationHeatMap(self):
        dataCorr = self.__data.copy()
        if self.__isToCorrelateWithTargetColumn:
            dataCorr[self.__names[self.__columnY]] = dataCorr[self.__names[self.__columnY]].astype(float)
        correlationMatrix = dataCorr.corr() #this correlation function isnt affected by data reescaling
        self._correlationCsvMap(correlationMatrix)
        seaHeatGraphic = seaborn.heatmap(correlationMatrix,annot=True,fmt='.0%')
        figNumber = seaHeatGraphic.get_figure()
        plt.tight_layout()
        figNumber.savefig(self.__CORRELATION_GRAPHIC + self.__DATA_FORMAT, dpi=150)
        plt.close(figNumber)

    def _correlationCsvMap(self, correlationMatrix):
        names = list(correlationMatrix)
        file = open(self.__CORRELATION_GRAPHIC + '.csv','w')
        file.write('var/var;')
        for iName in names:
            file.write(iName + ';')
        file.write('\n')
        for i in range(len(correlationMatrix)):
            file.write(names[i] + ';')
            for j in range(len(correlationMatrix.iloc[i,:])):
                file.write(str(correlationMatrix.iloc[i,j]) + ';')
            file.write('\n')
        file.close()

        
# FOR NUMBERS
    def setNpoints(self, nPoints):
        self.__N_POINTS = nPoints
        
    def setOutliersCut(self, outliersCut):        
        self.__OUTLIERS_CUT = outliersCut
        
    def setFontSize(self, fontSize):
        self.__FONT_SIZE = fontSize

    def graphicInadimplenciaXContinuum(self, data, colName):
        xAxis, yAxis, allContracts = self._inadimplenciaXContinumFeature(data, colName)
        plt.rcParams.update({'font.size': self.__FONT_SIZE})
        fig = plt.figure()
        plt.plot(xAxis,yAxis, color = 'r')
        widthBar = (xAxis[1] - xAxis[0]) * 0.5
        print('xAxis:  ',xAxis,'\n')
        print('yAxis:  ',yAxis,'\n')
        plt.bar(xAxis, allContracts, width=widthBar)
        plt.xlabel(colName)
        plt.ylabel('Percentage (%)')        
        fig.savefig(colName + '-inadXcontinuum.png', dpi=200)

    def _inadimplenciaXContinumFeature(self, data, colName):
        adimValues, inadValues = breakColIntoAdimAndInad(colName, data)
        adimValues = removeOutliersWithLimits(adimValues,self.__OUTLIERS_CUT)
        inadValues = removeOutliersWithLimits(inadValues,self.__OUTLIERS_CUT)
        print('Contratos adimplentes:  ',len(adimValues))
        print('Contratos inadimlentes: ', len(inadValues))
        xMin = min([adimValues.min()[0],inadValues.min()[0]])
        xMax = max([adimValues.max()[0],inadValues.max()[0]])
        variation = (xMax - xMin) / (self.__N_POINTS - 1)
        xAxisValues = []    
        yAxisValues = []
        allContracts = []
        nContracts = 0
        for i in range(self.__N_POINTS):
            dx = variation * i
            if i != self.__N_POINTS - 1:
                xUpper = xMin + dx + 0.5*variation
            else:
                xUpper = xMin + dx + variation*1e-6
            if i != 0:
                xLower = xMin + dx - 0.5*variation
            else:
                xLower = xMin
            adimCount = 0
            for adimValue in adimValues.iloc[:,0]:
                if adimValue < xUpper and adimValue >= xLower:
                    adimCount += 1
            inadCount = 0
            for inadValue in inadValues.iloc[:,0]:            
                if inadValue < xUpper and inadValue >= xLower:
                    inadCount += 1
            contracts = adimCount + inadCount
            if contracts == 0:
                continue
            else:
                xAxisValues.append(xMin + dx)
                inadPercentages = round(100*inadCount/contracts)
                yAxisValues.append(inadPercentages)
                allContracts.append(contracts)
                nContracts += contracts
        allContracts = [round(100*x / nContracts) for x in allContracts]
        return [xAxisValues,yAxisValues, allContracts]
        
#################################################################################

class CategoryCharacteristics:
    def __init__(self):
        self.__allCatDefaultNumbers = []
        self.__allCatNonDefaultNumbers = []
        self.__totalCount = []
        self.__allPercentages = []
        self.__allLabels = []
        
    def addValues(self, category, nDefault, nTotal):
        self.__allCatDefaultNumbers.append(nDefault)
        self.__allCatNonDefaultNumbers.append(nTotal - nDefault)
        self.__totalCount.append(nTotal)
        if nTotal != 0:
            percentage = str(round(100*nDefault/nTotal)) + '%'
        else:
            percentage = '0%'
        self.__allPercentages.append(percentage)
        self.__allLabels.append(category)
        
    def getAllCatDefaultNumbers(self):
        return self.__allCatDefaultNumbers
    
    def getAllCatNonDefaultNumbers(self):
        return self.__allCatNonDefaultNumbers
    
    def getTotalCount(self):
        return self.__totalCount
    
    def getAllPercentages(self):
        return self.__allPercentages
    
    def getAllLabels(self):
        return self.__allLabels

#################################################################################

if __name__ == "__main__":
    print('DataExploration')
    
