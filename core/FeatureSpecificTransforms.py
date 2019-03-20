import pandas
import numpy

class FeatureSpecificTransforms:
    def __init__(self):
        pass
        
    def getColumnsToFloat(self, transformType):
        if transformType == "createdataComproFeature":
            return ['Valor Renda Banco Semear Consulta Proposta JRetail PF ',
                    'Valor Renda do c njuge Banco Semear Consulta Proposta JRetail PF ',
                    'Valor Parcela da compra Banco Semear Consulta Proposta JRetail PF ',
                    'Valor Parcelas em aberto Banco Semear Consulta Proposta JRetail PF ',
                    'Valor D bito 1 Unitfour Consulta INSS por CPF PF ',
                    'Valor D bito 2 Unitfour Consulta INSS por CPF PF ',
                    'Valor D bito 3 Unitfour Consulta INSS por CPF PF ',
                    'Valor D bito 4 Unitfour Consulta INSS por CPF PF ',
                    'Valor D bito 5 Unitfour Consulta INSS por CPF PF ',
                    'Valor D bito 6 Unitfour Consulta INSS por CPF PF ']
        else:
            raise Exception('getColumnsToFloat: Specific transform not found')
    
        
    def createdataComproFeature(self, data):
        renda = 'Valor Renda Banco Semear Consulta Proposta JRetail PF '
        rendaCon = 'Valor Renda do c njuge Banco Semear Consulta Proposta JRetail PF '
        parcCompra = 'Valor Parcela da compra Banco Semear Consulta Proposta JRetail PF '
        parcAberto = 'Valor Parcelas em aberto Banco Semear Consulta Proposta JRetail PF '
        deb1 = 'Valor D bito 1 Unitfour Consulta INSS por CPF PF '
        deb2 = 'Valor D bito 2 Unitfour Consulta INSS por CPF PF '
        deb3 = 'Valor D bito 3 Unitfour Consulta INSS por CPF PF '
        deb4 = 'Valor D bito 4 Unitfour Consulta INSS por CPF PF '
        deb5 = 'Valor D bito 5 Unitfour Consulta INSS por CPF PF '
        deb6 = 'Valor D bito 6 Unitfour Consulta INSS por CPF PF '
        data.loc[:,renda] = data.loc[:,renda].fillna(0)
        data.loc[:,rendaCon] = data.loc[:,rendaCon].fillna(0)
        data.loc[:,parcCompra] = data.loc[:,parcCompra].fillna(0)
        data.loc[:,parcAberto] = data.loc[:,parcAberto].fillna(0)
        data.loc[:,deb1] = data.loc[:,deb1].fillna(0)
        data.loc[:,deb2] = data.loc[:,deb2].fillna(0)
        data.loc[:,deb3] = data.loc[:,deb3].fillna(0)
        data.loc[:,deb4] = data.loc[:,deb4].fillna(0)
        data.loc[:,deb5] = data.loc[:,deb5].fillna(0)
        data.loc[:,deb6] = data.loc[:,deb6].fillna(0)
        data['dataComproDeb'] = data.loc[:,parcCompra] + data.loc[:,parcAberto] + data.loc[:,deb1] + data.loc[:,deb2] + data.loc[:,deb3] + data.loc[:,deb4] + data.loc[:,deb5] + data.loc[:,deb6]
        data['dataComproDivisionDeb'] = data['dataComproDeb'].truediv(data.loc[:,renda] + data.loc[:,rendaCon])
        return data

        


#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################


