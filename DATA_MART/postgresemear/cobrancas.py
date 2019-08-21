import psycopg2
import datetime
import pandas as pd

def crie_conexao_sql():
    conexao = psycopg2.connect(user = "postgres",
                                  password = "Bolota",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "cobrancas")
    cursor = conexao.cursor()
    return [conexao, cursor]

def feche_conexao_sql(conexao, cursor):
    if(conexao):
        conexao.close()
        cursor.close()
        
def execute_query(query):
    conexao, cursor = crie_conexao_sql()
    cursor.execute(query)
    conexao.commit()
    feche_conexao_sql(conexao, cursor)

def adicione_multiplos_registros(query, registros):
    conexao, cursor = crie_conexao_sql()
    cursor.executemany(query, registros)
    conexao.commit()
    feche_conexao_sql(conexao, cursor)

def query_para_pandas(query, parametros = ''):
    conexao, cursor = crie_conexao_sql()
    if len(parametros) == 0:
        cursor.execute(query)
    else:
        cursor.execute(query, parametros)
    conexao.commit()
    registros = []
    for registro in cursor:
        registros.append(registro)
    feche_conexao_sql(conexao, cursor)
    return pd.DataFrame(data=registros)

def query_max_coluna(nome_coluna, nome_tabela):
    try:
        query_max = "SELECT MAX(" + nome_coluna + ") FROM " + nome_tabela
        return int(query_para_pandas(query_max).iloc[0,0])
    except (Exception, psycopg2.Error) as error :
        print ("ERRO:\n   ", error)
        return None

