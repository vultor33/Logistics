import re
import numpy as np

def converte_latin_para_float(valor):
    ''' Recebe um numero no formato latino e o converte em um
        valor numerico '''
    if e_nulo(valor):
        return np.nan
    valor = str(valor).replace('.','')
    valor = str(valor).replace(',','.')
    return float(valor)

def e_nulo(valor):
    valor_string = str(valor).lower()
    if valor_string == 'nan' or valor_string == 'none' or valor_string == 'nat':
        return True
    else:
        return (valor is np.nan or valor != valor)

def remove_caracteres_especiais(valor):
    return re.sub('[^A-Za-z0-9]+', ' ', str(valor))

def limpa_nome_das_colunas(dados):
    """ Remove todos os caracteres especias das colunas de uma dada tabela.
        A tabela dados precisa ser um objeto do tipo pandas """
    novos_nomes = []
    for col in dados.columns:
        novos_nomes.append(remove_caracteres_especiais(col))
    dados.columns = novos_nomes
    return dados

def cpf_para_inteiro(cpfString):
    """ Transforma o cpf no formato 024.145.145-17 em um numero inteiro """
    cpfString = cpfString.replace('.','')
    cpfString = cpfString.replace('-','')
    return int(cpfString)    

def coluna_cpf_para_inteiro(dados, coluna):
    dados[coluna] = dados.loc[:,coluna].apply(cpf_para_inteiro)
    return dados    