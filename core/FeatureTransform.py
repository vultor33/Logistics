import pandas
import numpy
import datetime

from core.FeatureSpecificTransforms import FeatureSpecificTransforms

class FeatureTransform:
    def __init__(self):
        self.__NOW = datetime.datetime.now()
        self.__DATE_REFERENCE_COLUMN = []
        self.__featTransforms = FeatureSpecificTransforms()
        
    def transform(self, data, colName, options):
        options = options[colName]
        if options['type'] == 'cat':
            data = self.catTransforms(data, colName, options['transforms'])
        elif options['type'] == 'float':
            data = self.floatTransforms(data,colName,options['transforms'])
        return data

    def getAllColumnsNames(self, allOptions):
        allColumnsNames = []
        for col in allOptions:
            if allOptions[col]['type'] == 'cat':
                for cat in allOptions[col]['transforms']['oneHotColumns']:
                    allColumnsNames.append(col + ':' + cat)
            else:
                allColumnsNames.append(col)
        return allColumnsNames

############################################################################################################    
    
    def catTransforms(self, data, colName, options):
        data.index = range(len(data))
        data.loc[:,colName] = data.loc[:,colName].fillna(options['fillna'])
        self.transformCategories(data.loc[:,colName],options['convertCategories'])
        data = self.oneHotEncoder(data,colName,options['oneHotColumns'])
        return data

    def oneHotEncoder(self, data, colName, oneHotColumns):
        columnsEncoded = self._calculateOneHotEncoderColumns(data, colName, oneHotColumns)
        for col in oneHotColumns:
            data[colName + ':' + col] = columnsEncoded[col]
        data = data.drop(colName,axis=1)
        return data
        
    def _calculateOneHotEncoderColumns(self, data, colName, oneHotColumns):
        columnsEncoded = {}
        for col in oneHotColumns:
            columnsEncoded[col] = []
        for element in data.loc[:,colName]:
            for col in columnsEncoded:
                if element == col:
                    columnsEncoded[col].append(1)
                else:
                    columnsEncoded[col].append(0)
        return columnsEncoded

############################################################################################################    

    def floatTransforms(self, data, colName, options):
        data = self.floatTypeTransform(data, colName, options['floatType'])
        data.loc[:,colName] = data.loc[:,colName].fillna(options['fillna'])
        data.loc[:,colName] = self.numberOperations(data.loc[:,colName], options['numberOperations'])
        data = self.removeOutliersWithLimits(data,colName, options['outliersCut'])  # saber quantas amostras foram eliminadas aqui
        return data
        
    def floatTypeTransform(self, data, colName, option):
        if option == 'convertStringToFloatLatin':
            self.convertStringToFloatLatin(data.loc[:,colName])
        elif option == 'convertRelativeDateDays':
            self.convertRelativeDateDays(data.loc[:,colName])
        elif option == 'createdataComproFeature':
            colsToFloat = self.__featTransforms.getColumnsToFloat('createdataComproFeature')
            for colName in colsToFloat:
                data = self.floatTypeTransform(data, colName, 'convertStringToFloatLatin')
            data = self.__featTransforms.createdataComproFeature(data)
        return data
        
    def numberOperations(self, columnToConvert, operations):
        for operation in operations:
            operation = operation.split('-')
            if len(operation) != 2:
                raise Exception('ON FeatureTransform.numberOperations, operation: ' + str(operation) + 'format is not correct' )
            if operation[0] == 'divide':
                columnToConvert = columnToConvert/float(operation[1])
        return columnToConvert


############################################################################################################    

    def convertStringToFloatLatin(self, columnToConvert):
        for i in columnToConvert.index:
            try:
                columnToConvert.at[i] = self._floatLatin(columnToConvert.loc[i])
            except:
                raise Exception('ON:FeatureTransform.convertStringToFloatLatin,  VALUE:  ' + str(columnToConvert.at[i]) + ' IS NOT A FLOAT')
        columnToConvert = columnToConvert.astype(float)

    def _floatLatin(self, entry):
        if self._isNan(entry):
            return numpy.nan
        entry = str(entry).replace(',','.')
        return float(entry)

    def _isNan(self, entry):
        if isinstance(entry, str):
            return entry == 'nan'
        else:
            return numpy.isnan(entry)

############################################################################################################

    def setDateReference(self, referenceColumn):
        self.convertDateToFloatLatinDays(referenceColumn)
        self.__DATE_REFERENCE_COLUMN = referenceColumn.copy()

    def convertRelativeDateDays(self, columnDate):
        if len(self.__DATE_REFERENCE_COLUMN) == 0:
            raise Exception('ON:convertRelativeDateDays, set DATE_REFERENCE_COLUMN first')
        self.convertDateToFloatLatinDays(columnDate)
        return columnDate - self.__DATE_REFERENCE_COLUMN

    def convertDateToFloatLatinDays(self, columnToConvert):
        for i in columnToConvert.index:
            try:
                columnToConvert.at[i] = self._calculateAgeInDays(columnToConvert.loc[i])
            except:
                raise Exception('ON:FeatureTransform.convertDateToFloatLatin,  VALUE:  ' + str(columnToConvert.at[i]) + ' IS NOT A DATE')
        columnToConvert = columnToConvert.astype(float)

    def _calculateAgeInDays(self, strDate):
        strFormat = self._getDate(strDate)
        try:
            day = strFormat[0]
            month = strFormat[1]
            year = strFormat[2]
            return (self.__NOW - datetime.datetime(year,month,day)).days
        except:
            return numpy.nan                

    def _getDate(self, dateStr):  #dateStr.split('/') would be easier
        if self._isNan(dateStr):
            return numpy.nan
        day = ''
        month = ''
        year = ''
        flag = 'readDay'
        for iChar in dateStr:
            if iChar == ' ':
                break
            elif iChar == '/':
                if flag == 'readDay':
                    flag = 'readMonth'
                elif flag == 'readMonth':
                    flag = 'readYear'
            elif flag == 'readDay':
                day += iChar
            elif flag == 'readMonth':
                month += iChar
            elif flag == 'readYear':
                year += iChar
        return [int(day),int(month),int(year)]

    
############################################################################################################

    def transformCategories(self, columnToConvert, catTransforms):
        for i in columnToConvert.index:
            for cat in catTransforms:
                if columnToConvert.at[i] == cat:
                    columnToConvert.at[i] = catTransforms[cat]
                    
############################################################################################################
                                    
    def removeOutliersWithLimits(self, data, columnName, outliersLimits):
        if len(outliersLimits) == 0:
            return data
        columnToRemove = data.loc[:,columnName]
        if outliersLimits[0] != None:
            indexCut = self._removeOutliers(columnToRemove, outliersLimits[0], 'lower')
            data = data.drop(indexCut)
        if outliersLimits[1] != None:
            indexCut = self._removeOutliers(columnToRemove, outliersLimits[1], 'greater')
            data = data.drop(indexCut)
        return data
                    
    def _removeOutliers(self, columnToRemove, cutValue, flag):
        if flag == 'greater':
            return columnToRemove[columnToRemove.values > cutValue].index
        elif flag == 'lower':
            return columnToRemove[columnToRemove.values < cutValue].index

        
        
        
                    