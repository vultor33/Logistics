import datetime
import dwsemear
import postgresemear as sql

def adiciona_responsavel(dados):
    ''' Esta adicao usa 2 colunas como referencia:
        Se o campo Responsavel for nulo, deve-se adicionar
        a informacao presente no campo Assessoria e vice versa.
        Todos os responsaveis possuem um codigo unico que aparece
        na tabela responsavel do banco de dados cobrancas'''
    tabela_responsavel = responsaveis_sem_acento()
    todos_id_responsavel = []
    for i in dados.index:
        responsavel = encontre_responsavel(i, dados)
        tabela_com_id_responsavel = tabela_responsavel[tabela_responsavel.loc[:,'Nome'] == responsavel]
        if len(tabela_com_id_responsavel) != 1:
            raise Exception("O responsavel pelo acionamento da linha " + str(i) + " nao esta cadastrado")
        id_responsavel = int(tabela_com_id_responsavel.iloc[0,0])
        todos_id_responsavel.append(id_responsavel)
    dados['responsavel_acionamento'] = todos_id_responsavel
    return dados
    
def encontre_responsavel(i, dados):
    responsavel = str(dados.loc[i,'Respons vel'])
    if responsavel == 'nan':
        responsavel = dados.loc[i,'Assessoria']
    responsavel = dwsemear.remove_caracteres_especiais(responsavel)
    responsavel = responsavel.lower()
    return responsavel
    
def responsaveis_sem_acento():
    responsaveis_acionamentos = sql.query_para_pandas('SELECT * FROM responsavel')
    responsaveis_acionamentos.columns = ['IDResponsavel', 'FuncaoDoResponsavel', 'Empresa', 'Nome']
    nomes_sem_acentos = []
    for i in responsaveis_acionamentos.index:
        nome = responsaveis_acionamentos.loc[i, 'Nome']
        nome = dwsemear.remove_caracteres_especiais(nome)
        nome = nome.lower()
        nomes_sem_acentos.append(nome)
    responsaveis_acionamentos['Nome'] = nomes_sem_acentos
    return responsaveis_acionamentos

##########################################################################################

def geracao_coluna_datahora(dados):
    """ A partir da coluna 'Data' e da coluna 'Horario' e criado um
        objeto do tipo datetime """
    datahora = []
    for i in dados.index:
        datahora.append(dados.loc[i,'Data'] + ' ' + dados.loc[i,'Hor rio'])
    dados['datahora'] = datahora
    dados['datahora'] = dados['datahora'].apply(data_para_datetime)
    return dados

def data_para_datetime(string_data):
    return datetime.datetime.strptime(string_data, '%d/%m/%Y %H:%M') 

##########################################################################################

def corrige_campo_observacoes(dados):
    """ Na tabela de acionamentos gerada no Semear os \n do campo observacoes
        se propaga na tabela criando linhas vazias.
        Essa funcao tem como objetivo remover as linhas vazias e coletar as observacoes
        que apareceram nessas linhas """
    cpf_nulo = dados[dados.loc[:,'CPF CNPJ'].isnull()].index
    for i in cpf_nulo:
        iObs = localize_linha_preenchida(i, cpf_nulo)
        novas_observacoes = pegar_observacoes(dados.loc[i,:].tolist())
        dados.loc[iObs,'Observa es'] += ' ' + novas_observacoes
    dados = dados.drop(cpf_nulo)
    dados = dados.reset_index(drop=True)
    return dados
        
def pegar_observacoes(linha):
    observacoes = ''
    for elem in linha:
        if str(elem) != 'nan':
            observacoes += elem + ' '
    return observacoes

def localize_linha_preenchida(i, cpf_nulo):
    k = i
    while(k >= 0):
        k -= 1
        if k not in cpf_nulo:
            return k
    raise Exception("Erro na funcao: localize_linha_preenchida - Linha preenchida nao encontrada")
        