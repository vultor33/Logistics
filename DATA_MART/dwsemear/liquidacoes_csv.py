

def separa_codigo_do_contrato(dados):
    contratos = []
    renegociacoes = []
    for i in dados.index:
        codigo_contrato, codigo_renegociacao = dados.loc[i,'Contrato'].split('/')
        contratos.append(codigo_contrato)
        renegociacoes.append(codigo_renegociacao)
    dados['codigos_contratos'] = contratos
    dados['codigos_renegociacoes'] = renegociacoes
    return dados
    
def separa_forma_liquidacao(dados):
    codigo_da_forma_de_liquidacao = []
    descricao_da_forma_de_liquidacao = []
    for i in dados.index:
        forma_de_liquidacao = str(dados.loc[i,'Forma'])
        if forma_de_liquidacao == 'nan':
            codigo_da_forma_de_liquidacao.append(None)
            descricao_da_forma_de_liquidacao.append(None)
        else:
            codigo_da_forma_de_liquidacao.append(int(forma_de_liquidacao.split(' ')[0]))
            descricao_da_forma_de_liquidacao.append(forma_de_liquidacao)
    return codigo_da_forma_de_liquidacao, descricao_da_forma_de_liquidacao    

def separa_codigo_produto(dados):
    produtos_codigos = []
    produtos_descricoes = []
    for i in dados.index:
        prod = dados.loc[i,'Produto']
        prod_codigo = int(prod.split(' ')[0])
        prod_descr = prod
        produtos_codigos.append(prod_codigo)
        produtos_descricoes.append(prod_descr)
    dados['produtos_codigos'] = produtos_codigos
    dados['produtos_descricoes'] = produtos_descricoes
    return dados
        