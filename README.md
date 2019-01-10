# rankingcbf
Calculadora de pontos para o Ranking Nacional de Clubes da CBF.

O cálculo dos pontos dos clubes brasileiros de futebol para o Ranking Nacional da CBF é feito a partir de uma compilação de resultados em um arquivo do Excel (posrankingcbf.xlsx). 
Este arquivo é lido por um script em python e, dado o ano de referência na função, esta retorna dois rankings: o de clubes e o de federações.

As funções em calcularanking.py são:

- calcularanking(ano): retorna uma tupla contendo dois dataframes do Pandas, sendo o primeiro o Ranking Nacional de Clubes e o segundo, o Ranking Nacional de Federações.

- ranking_arquivo(ano): tem o mesmo retorno da função anterior, mas também cria um arquivo do Excel com o título Ranking CBF <<ano>>.xlsx, contendo os dois rankings gerados em tabelas separadas.
  
Observações:
- a base de dados disponível para o cálculo deste ranking é válido para os anos de 2017 a 2019.
- o Ranking da CBF é calculado a partir dos resultados dos cinco anos anteriores.


Referências:

Divulgação do Ranking 2019:
https://www.cbf.com.br/futebol-brasileiro/noticias/campeonato-brasileiro/palmeiras-assume-ponta-isolada-do-ranking-nacional-de-clubes-da-cbf

Critérios para cálculos:
https://conteudo.cbf.com.br/cdn/201812/20181205143339_271.pdf
