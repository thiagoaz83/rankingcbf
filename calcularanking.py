# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 17:13:39 2017

@author: Thiago

Automatização da criação do Ranking da CBF de clubes e de federações a partir de uma base de dados no formato excel.
Cálculo válido para rankings a partir do ano de 2016.
"""

import pandas as pd
import numpy as np
arquivo = "posrankingcbf.xlsx" #base de dados com os resultados de cada equipe

#Carrega as tabelas do arquivo de dados do Excel em formato pandas
pontos = pd.read_excel(arquivo, sheetname = "Pontos", index_col = None)
bonus = pd.read_excel(arquivo, sheetname = "Bônus", index_col = None)
brasileirao = pd.read_excel(arquivo, sheetname = "Brasileirão", index_col = None)
copadobrasil = pd.read_excel(arquivo, sheetname = "Copa do Brasil", index_col = None)

#Cria dicionário com os multiplicadores de valores do Brasileirão por divisão
#Transforma dicionário em série, para posterior insersão na tabela
multiplica_serie = {"Série A": 8, "Série B": 4, "Série C": 2, "Série D": 1}
multi = pd.Series(multiplica_serie, name = "MultiSéries")

#Classifica a tabela de pontos a partir da competição e da posição
pontos.set_index(["Campeonato", "Class"], inplace=True)

#Cria a coluna de pontuação da Copa do Brasil, a partir da criação de uma coluna temporária
copadobrasil["tmp"] = "Copa do Brasil"
copadobrasil = copadobrasil.join(pontos, on = ["tmp", "Posição"])
copadobrasil.drop("tmp", axis = 1, inplace = True)

#Cria a coluna de pontuação do Campeonato Brasileiro, a partir da criação de uma coluna temporária
brasileirao["tmp"] = "Brasileirão"
brasileirao = brasileirao.join(pontos, on = ["tmp", "Posição"])
brasileirao.drop("tmp", axis = 1, inplace = True)
#Substitui os pontos invalidos pelo valor mínimo
brasileirao.Pontos.fillna(pontos.loc["Brasileirão", "min"].Pontos, inplace=True)
#Multiplica a pontuação de acordo com a série
brasileirao = brasileirao.join(multi, on = "Campeonato")
brasileirao.Pontos = brasileirao.Pontos * brasileirao.MultiSéries
brasileirao.drop("MultiSéries", axis = 1, inplace = True)

#Cria um dataframe final com times, anos e pontuações
listapontos = ["Time", "UF", "Ano", "Pontos"]
pontostotal = pd.concat([brasileirao[listapontos], copadobrasil[listapontos], bonus[listapontos]], ignore_index=True)

def calcularanking(ano, pb = pontostotal):
    #Dado o ano, carrega o total de pontos e dá como resultado os rankings de clubes e de federações, na ordem.
    
    pontosbase = pb.copy() #Cópia da lista total de pontos
    
    #Atribui pesos aos pontos de acordo com o ano e descarta resultados fora do prazo.
    pontosbase.Ano = 5 + pontosbase.Ano - ano
    pontosbase = pontosbase[(pontosbase.Ano > 0) & (pontosbase.Ano <= 5)]
    pontosbase.Pontos = pontosbase.Pontos * pontosbase.Ano
    pontosbase.drop("Ano", axis = 1, inplace = True)
    pontosbase.Pontos = pontosbase.Pontos.astype(np.int64)
    
    #Cria o ranking de clubes a partir da soma por time e o ordena.
    rktimes = pontosbase.groupby(["Time", "UF"]).sum()
    rktimes.sort_values("Pontos", ascending = False, inplace = True)
    rktimes.reset_index(inplace = True)
    rktimes["Posição"] = rktimes["Pontos"].rank(ascending = False, method = "min")
    rktimes["Posição"] = rktimes["Posição"].astype(np.int64)
    lt = ["Posição", "Time", "UF", "Pontos"]
    rktimes = rktimes[lt]
    
    #Cria o ranking de federações a partir da soma de clubes do mesmo estado e o ordena.
    rkufs = pontosbase.groupby("UF").sum()
    rkufs.sort_values("Pontos", ascending = False, inplace = True)
    rkufs.reset_index(inplace = True)
    rkufs["Posição"] = rkufs["Pontos"].rank(ascending = False, method = "min")
    rkufs["Posição"] = rkufs["Posição"].astype(np.int64)
    ut = ["Posição", "UF", "Pontos"]
    rkufs = rkufs[ut]
    
    return rktimes, rkufs

def ranking_arquivo(ano):
    #Cria os rankings e retorna também um arquivo do excel com cada um deles em uma tabela.
    nome = "Ranking CBF {0}.xlsx".format(str(ano))

    times, uf = calcularanking(ano)
    
    writer = pd.ExcelWriter(nome)
    
    times.to_excel(writer, index = False, sheet_name = "Ranking Clubes")
    uf.to_excel(writer, index = False, sheet_name = "Ranking Federações")
    writer.save()
    
    return times, uf