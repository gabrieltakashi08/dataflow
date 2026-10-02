import pandas as pd
from visualizacoes.graficos import (
    grafico_faturamento_mensal,
    grafico_faturamento_cidade,
    grafico_ticket_medio_cidade
)
clientes = pd.read_csv("data/raw/clientes.csv")
vendas = pd.read_csv("data/raw/vendas.csv")
clientes["data_cadastro"] = pd.to_datetime(clientes["data_cadastro"])
vendas["data venda"] = pd.to_datetime(vendas["data venda"])

vendas["ano"] = vendas["data venda"].dt.year
vendas["mes"] = vendas["data venda"].dt.month
vendas["mes_ano"] = vendas["data venda"].dt.to_period("M")
vendas["valor total"] = vendas["valor total"].round(2)

faturamento_total = vendas["valor total"].sum().round(2)
faturamento_mensal = vendas.groupby("mes_ano")["valor total"].sum().round(2)
faturamento_mensal = faturamento_mensal.sort_index()
maior_venda = vendas["valor total"].max()
menor_venda = vendas["valor total"].min()
desvio_padrao = vendas["valor total"].std()
mediana_venda = vendas["valor total"].median()
venda_por_mes = vendas.groupby("mes_ano").size()
media_de_vendas = venda_por_mes.mean()
faturamento_max_mes = faturamento_mensal.max()
faturamento_min_mes = faturamento_mensal.min()
ticket_medio = vendas["valor total"].sum()
ticket_medio = vendas["valor total"].mean()
quantidade_vendas = len(vendas)
crescimento_mensal = faturamento_mensal.pct_change()*100

print("faturamento total:", faturamento_total)
print("faturamento mensal:")
print(faturamento_mensal)
print("faturamento total:", round(faturamento_total,2))
print("ticket_medio:", round(ticket_medio,2))
print("quantidade_vendas:", quantidade_vendas)
print("maior venda:", round(maior_venda,2))
print("menor venda:", round(menor_venda,2))
print("mediana das vendas:", round(mediana_venda,2))
print("desvio padrão:", round(desvio_padrao,2))
print("media de vendas por mes:", round(media_de_vendas,2))
print("maior faturamento mensal:", round(faturamento_max_mes,2))
print("faturamento mínimo mensal", round(faturamento_min_mes,2))
print("crescimento mensal(%):", round(crescimento_mensal,2))
print(vendas.columns)
print(clientes.columns)

vendas_clientes = vendas.merge(clientes, left_on="cliente ID", right_on="ID", how="left")
print("\n vendas + clientes")
vendas_clientes = vendas_clientes.drop(columns=["ID_y"])
vendas_clientes = vendas_clientes.rename(columns={"ID_x": "ID"})

vendas_clientes.to_csv(  "data/processed/vendas_clientes.csv", index=False)

print(vendas_clientes.head())
print(vendas_clientes.columns)
print(vendas_clientes.isnull().sum())

faturamento_clientes = (vendas_clientes.groupby("nome")["valor total"].sum().sort_values(ascending=False))
print("\nfaturamento por cliente")
print(faturamento_clientes)

faturamento_cidade = vendas_clientes.groupby("cidade")["valor total"].sum().sort_values(ascending=False)
print("\nfaturamento por cidade")
print(faturamento_cidade)

vendas_por_cidade = vendas_clientes.groupby("cidade")["ID"].count().sort_values(ascending=False)
print("\nquantidade de vendas por cidade")
print(vendas_por_cidade)

ticket_medio_cidade = vendas_clientes.groupby("cidade")["valor total"].mean().round(2).sort_values(ascending=False)
print("\nticket médio por cidade")
print(ticket_medio_cidade)

grafico_faturamento_mensal(faturamento_mensal)
grafico_faturamento_cidade(faturamento_cidade)
grafico_ticket_medio_cidade(ticket_medio_cidade)
