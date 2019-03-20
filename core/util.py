import os
import re
import numpy 
import pandas
import datetime
import collections
from matplotlib import colors as mcolors
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.metrics import cohen_kappa_score

def getAbsolutePath(fileName):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, '../../' + fileName)

def removeSpecialCharacters(value):
    return re.sub('[^A-Za-z0-9]+', ' ', str(value))

def searchInData(data, refString):
    refString = removeSpecialCharacters(refString)
    for x in data:
        if refString in x:
            print(x)

def cleanDataColumns(data):
    trueCol = []
    for col in data.columns:
        trueCol.append(removeSpecialCharacters(col))
    data.columns = trueCol
    return data

def cleanCpf(cpfString):
    cpfString = cpfString.replace('.','')
    cpfString = cpfString.replace('-','')
    return int(cpfString)    

def renameColumn(data, oldColumnName, newColumnName):
    columns = list(data.columns)
    if oldColumnName not in columns:
        print('Couldnt find ',oldColumnName)
        return
    colIndex = columns.index(oldColumnName)
    columns[colIndex] = newColumnName
    data.columns = columns


def isDuplicatesPresent(column):
    L = list(column)
    most_common,num_most_common = collections.Counter(L).most_common(1)[0]
    return num_most_common > 1
    
###############################################################################################################3
# TALVEZ APARECAM EM OUTROS LUGARES
###############################################################################################################3

def _convertStringToFloatLatin(columnToConvert):
    for i in columnToConvert.index:
        try:
            columnToConvert.at[i] = _floatLatin(columnToConvert.loc[i])
        except ValueError:
            print('IN COL:  ',col, '  VALUE:  ', columnToConvert.at[i], ' IS NOT A FLOAT')
            return
    columnToConvert = columnToConvert.astype(float)
    return columnToConvert

def _floatLatin(entry):
    if _isNan(entry):
        return numpy.nan
    entry = str(entry).replace(',','.')
    return float(entry)

def _isNan(value):
    if isinstance(value, str):
        return value == 'nan'
    else:
        return numpy.isnan(value)

def _convertDateToAgeInYears(data, colName):
    _convertDateToFloatLatin(data,[colName])
    data.loc[:,colName] = data.loc[:,colName] - data.loc[:,' Data']
    data.loc[:,colName] = data.loc[:,colName]/365
    return data


def _convertDateToFloatLatin(data, dateColumns):
    for col in dateColumns:
        columnToConvert = data.loc[:,col]
        for i in columnToConvert.index:
            try:
                columnToConvert.at[i] = _calculateAge(columnToConvert.loc[i])
            except:
                print('IN COL:  ',col, '  VALUE:  ', columnToConvert.at[i], ' IS NOT A DATE')
                return
        data[col] = data.loc[:,col].astype(float)

def _getDate(dateStr):
    if _isNan(dateStr):
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

def _calculateAge(strDate):
    strFormat = _getDate(strDate)
    try:
        day = strFormat[0]
        month = strFormat[1]
        year = strFormat[2]
        return (datetime.datetime.now() - datetime.datetime(year,month,day)).days
    except:
        return numpy.nan                

def predictionsSum(pred, pagoTest, atrasoTest):
    sumPago = 0.0
    sumAtraso = 0.0
    for i in range(len(pred)):
        if pred[i] == '0':
            sumPago += float(pagoTest[i])
            sumAtraso += float(atrasoTest[i])
    return [sumPago, sumAtraso]

def inadimplenciaEmReais(prediction):
    testCols = dp.getTestSavedColumns()
    [pago, atraso] = predictionsSum(pred, testCols['VlrPago'], testCols['VlrEmAtraso'])
    accuracy = (pred == dp.getYtest())
    countPred = collections.Counter(prediction)
    aceites = countPred['0']
    print('aceites:  ', aceites)
    print('acuracia:  ',round((accuracy.mean())*100),'%')
    print('Inadimplencia:  ', round(100*atraso/pago),'%')
    print('prejuizo absoluto:  ', round(atraso/1e6,2), ' milhoes')
    print('prejuizo por numeros de aceites:  ', atraso/aceites, ' reais')
    
def printFeaturesImportances(dp, model):
    xtestCols = list(dp.getXtest().columns)
    colsImport = model.feature_importances_
    for xCols,colsImp in zip(xtestCols,colsImport):
        print(xCols, '  ',round(100*colsImp,1),'%') 

def calculateComprometimentoDeRenda(data):
    comprometimento = []
    for i in data.index:
        pclAbe = float(data.loc[i,'Valor Parcelas em aberto Banco Semear Consulta Proposta JRetail PF '])
        pclCompra = float(data.loc[i,'Valor Parcela da compra Banco Semear Consulta Proposta JRetail PF '])
        renda = float(data.loc[i,'Valor Renda Banco Semear Consulta Proposta JRetail PF '])
        compRenda = (pclAbe + pclCompra) / renda
        comprometimento.append(compRenda)
    data['comprometimento'] = comprometimento
    data = data.drop(['Valor Parcelas em aberto Banco Semear Consulta Proposta JRetail PF '],axis=1)
    data = data.drop(['Valor Parcela da compra Banco Semear Consulta Proposta JRetail PF '],axis=1)
    data = data.drop(['Valor Renda Banco Semear Consulta Proposta JRetail PF '],axis=1)
    return data
                 

def breakColIntoAdimAndFraud(colName, data, targetCol = 'Inadimplente'):
    colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
    x = data.loc[:,[colName,targetCol]].copy()
    nanIndexes = pandas.isnull(x).any(1).nonzero()[0]
    x = x.drop(nanIndexes)
    x = x.drop([targetCol],axis=1)
    y = data.loc[:,targetCol].copy()
    y = y.drop(nanIndexes)
    adimI = y[y=='0'].index
    inadI = y[y=='1'].index
    notFraudInd = data[data.loc[:,'VlrPago'] != 0].index    
    y = y.drop(notFraudInd)
    inadFraudI = y[y=='1'].index
    xinad = x.loc[inadI].copy()
    xadim = x.loc[adimI].copy()
    inadFraud = x.loc[inadFraudI].copy()
    return [xadim, xinad,inadFraud]

def breakColIntoAdimAndInad(colName, data, targetCol = 'Inadimplente'):
    colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
    x = data.loc[:,[colName,targetCol]].copy()
    nanIndexes = pandas.isnull(x).any(1).nonzero()[0]
    x = x.drop(nanIndexes)
    x = x.drop([targetCol],axis=1)
    y = data.loc[:,targetCol].copy()
    y = y.drop(nanIndexes)
    adimI = y[y=='0'].index
    inadI = y[y=='1'].index
    xinad = x.loc[inadI].copy()
    xadim = x.loc[adimI].copy()
    return [xadim, xinad]


def histogramPlotFraud(xadim, xinad, xFraud,  ylim = 2000):
    colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
    colName = list(xadim.columns)[0]                                  
    fig = plt.figure()
    plt.hist(numpy.array(xadim),color=colors['b'])
    plt.hist(numpy.array(xinad),color=colors['g'])
    plt.hist(numpy.array(xFraud),color=colors['r'])
    plt.ylabel('Count')
    plt.xlabel(colName)
    plt.ylim(0,ylim)
    fig.savefig('histogram--' + colName + '.png', dpi=150)
    
def removeOutliers(col, cutValue, flag='greater'):
    if flag == 'greater':
        indexCut = col[col.values > cutValue].index
        return col.drop(indexCut)
    elif flag == 'lower':
        indexCut = col[col.values < cutValue].index
        return col.drop(indexCut)
    
def removeOutliersWithLimits(xVector, outliersLimits):
    if len(outliersLimits) == 0:
        return xVector
    if outliersLimits[0] != None:
        xVector = removeOutliers(xVector, outliersLimits[0], 'lower')
    if outliersLimits[1] != None:
        xVector = removeOutliers(xVector, outliersLimits[1])
    return xVector

def printModelPredictionsSmartCredit(yReal, prediction):
    confusionMatrix = confusion_matrix(yReal,prediction)
    print('Inadimplencia final:  ', round(100*confusionMatrix[1][0] /(confusionMatrix[1][0] + confusionMatrix[0][0])),'%')
    print('Dos inadimplentes, acertei:  ',round(100*confusionMatrix[1][1] /(confusionMatrix[1][0] + confusionMatrix[1][1])),'%')
    print('Dos adimplentes, acertei:  ',round(100*confusionMatrix[0][0] /(confusionMatrix[0][0] + confusionMatrix[0][1])),'%')
    print('KAPPA:  ',cohen_kappa_score(yReal,prediction))
    confusionPlot(yReal, prediction)

def confusionPlot(Ytest, predictions):
    confusionMatrix = confusion_matrix(Ytest, predictions)
    print(confusionMatrix)
    seaPlot = sns.heatmap(confusionMatrix, square=True, annot=True, cbar=False)
    plt.xlabel('predicted value')
    plt.ylabel('true value')
    plt.show()

def generateScoreTable(model, dataX, dataY):
    dataX.index = range(len(dataX))
    dataPred = model.predict_proba(dataX)
    dataPred = pandas.DataFrame(data = dataPred)
    dataPred.columns = model.classes_
    dataPred['score'] = dataPred.loc[:,'0'] * 1000
    dataPred['Inadimplente'] = list(dataY)
    return dataPred
    
   