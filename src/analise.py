import pandas as pd

vendas_clientes = pd.read_csv(
    "data/processed/vendas_clientes.csv"
)

vendas_clientes["data venda"] = pd.to_datetime(
    vendas_clientes["data venda"]
)

print("Dataset carregado com sucesso!")
print("Linhas:", len(vendas_clientes))
print("Colunas:", len(vendas_clientes.columns))
faturamento_cliente = (
    vendas_clientes
    .groupby("nome")["valor total"]
    .sum()
    .round(2)
    .sort_values(ascending=False)
)

print("\nFaturamento por cliente:")
print(faturamento_cliente)
faturamento_cidade = (
    vendas_clientes
    .groupby("cidade")["valor total"]
    .sum()
    .round(2)
    .sort_values(ascending=False)
)

print("\nFaturamento por cidade:")
print(faturamento_cidade)

vendas_por_cidade = (
    vendas_clientes
    .groupby("cidade")["ID"]
    .count()
    .sort_values(ascending=False)
)

print("\nQuantidade de vendas por cidade:")
print(vendas_por_cidade)

ticket_medio_cidade = (
    vendas_clientes
    .groupby("cidade")["valor total"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
)

print("\nTicket médio por cidade:")
print(ticket_medio_cidade)

faturamento_mensal = (
    vendas_clientes
    .groupby("mes_ano")["valor total"]
    .sum()
    .round(2)
    .sort_index()
)

print("\nFaturamento mensal:")
print(faturamento_mensal)


crescimento_mensal = faturamento_mensal.pct_change() * 100

print("\nCrescimento mensal (%):")
print(crescimento_mensal.round(2))



faturamento_total = vendas_clientes["valor total"].sum().round(2)
ticket_medio = vendas_clientes["valor total"].mean().round(2)
maior_venda = vendas_clientes["valor total"].max().round(2)
menor_venda = vendas_clientes["valor total"].min().round(2)
mediana_venda = vendas_clientes["valor total"].median().round(2)
desvio_padrao = vendas_clientes["valor total"].std().round(2)
quantidade_vendas = len(vendas_clientes)

print("\nIndicadores gerais:")
print("Faturamento total:", faturamento_total)
print("Ticket médio:", ticket_medio)
print("Maior venda:", maior_venda)
print("Menor venda:", menor_venda)
print("Mediana das vendas:", mediana_venda)
print("Desvio padrão:", desvio_padrao)
print("Quantidade de vendas:", quantidade_vendas)


maior_faturamento_mes = faturamento_mensal.max()
menor_faturamento_mes = faturamento_mensal.min()

print("\nFaturamento mensal:")
print("Maior:", maior_faturamento_mes)
print("Menor:", menor_faturamento_mes)



vendas_por_mes = (
    vendas_clientes
    .groupby("mes_ano")
    .size()
)

print("\nQuantidade de vendas por mês:")
print(vendas_por_mes)


ticket_medio_mes = (
    vendas_clientes
    .groupby("mes_ano")["valor total"]
    .mean()
    .round(2)
)

print("\nTicket médio por mês:")
print(ticket_medio_mes)


participacao_cliente = (
    faturamento_cliente / faturamento_total * 100
).round(2)

print("\nParticipação dos clientes no faturamento (%):")
print(participacao_cliente)



top_5_clientes = faturamento_cliente.head(5)

print("\nTop 5 clientes:")
print(top_5_clientes)



participacao_top_5 = (
    top_5_clientes.sum() / faturamento_total * 100
).round(2)

print("\nParticipação dos 5 maiores clientes (%):")
print(participacao_top_5)


indice_maior_venda = vendas_clientes["valor total"].idxmax()

cliente_maior_venda = vendas_clientes.loc[
    indice_maior_venda, "nome"
]

valor_maior_venda = vendas_clientes.loc[
    indice_maior_venda, "valor total"
]

print("\nMaior venda individual:")
print("Cliente:", cliente_maior_venda)
print("Valor:", valor_maior_venda)

# Quantidade de compras por cliente
compras_por_cliente = (
    vendas_clientes
    .groupby("nome")["ID"]
    .count()
    .sort_values(ascending=False)
)

print("\nQuantidade de compras por cliente:")
print(compras_por_cliente)


# Ticket médio por cliente
ticket_medio_cliente = (
    vendas_clientes
    .groupby("nome")["valor total"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
)

print("\nTicket médio por cliente:")
print(ticket_medio_cliente)

faturamento_acumulado = faturamento_mensal.cumsum().round(2)

print("\nFaturamento acumulado:")
print(faturamento_acumulado)

crescimento_periodo = (
    (faturamento_mensal.iloc[-1] / faturamento_mensal.iloc[0]) - 1
) * 100

print("\nCrescimento entre primeiro e último mês:")
print(round(crescimento_periodo, 2), "%")

participacao_cidade = (
    faturamento_cidade / faturamento_total * 100
).round(2)

print("\nParticipação das cidades no faturamento (%):")
print(participacao_cidade)
# ==============================
# DATASETS ANALÍTICOS
# ==============================

# 1. Análise de clientes
clientes_analytics = pd.DataFrame({
    "faturamento": faturamento_cliente,
    "quantidade_compras": compras_por_cliente,
    "ticket_medio": ticket_medio_cliente
})

clientes_analytics["participacao_faturamento"] = (
    clientes_analytics["faturamento"] / faturamento_total * 100
).round(2)

clientes_analytics = clientes_analytics.sort_values(
    "faturamento",
    ascending=False
)

clientes_analytics.to_csv(
    "data/analytics/clientes_analytics.csv"
)


# 2. Análise mensal
mensal_analytics = pd.DataFrame({
    "faturamento": faturamento_mensal,
    "quantidade_vendas": vendas_por_mes,
    "ticket_medio": ticket_medio_mes,
    "crescimento_percentual": crescimento_mensal
})

mensal_analytics = mensal_analytics.round(2)

mensal_analytics.to_csv(
    "data/analytics/mensal_analytics.csv"
)


# 3. Análise por cidade
cidade_analytics = pd.DataFrame({
    "faturamento": faturamento_cidade,
    "quantidade_vendas": vendas_por_cidade,
    "ticket_medio": ticket_medio_cidade
})

cidade_analytics["participacao_faturamento"] = (
    cidade_analytics["faturamento"] / faturamento_total * 100
).round(2)

cidade_analytics = cidade_analytics.sort_values(
    "faturamento",
    ascending=False
)

cidade_analytics.to_csv(
    "data/analytics/cidade_analytics.csv"
)


print("\nDatasets analíticos gerados com sucesso!")
print("Arquivos:")
print("- data/analytics/clientes_analytics.csv")
print("- data/analytics/mensal_analytics.csv")
print("- data/analytics/cidade_analytics.csv")

# ==============================
# KPIs CONSOLIDADOS
# ==============================

kpis = pd.DataFrame({
    "indicador": [
        "Faturamento total",
        "Quantidade de vendas",
        "Ticket médio",
        "Maior venda",
        "Menor venda",
        "Mediana das vendas",
        "Desvio padrão",
        "Maior faturamento mensal",
        "Menor faturamento mensal",
        "Crescimento do período",
        "Participação dos 5 maiores clientes"
    ],
    "valor": [
        faturamento_total,
        quantidade_vendas,
        ticket_medio,
        maior_venda,
        menor_venda,
        mediana_venda,
        desvio_padrao,
        maior_faturamento_mes,
        menor_faturamento_mes,
        round(crescimento_periodo, 2),
        participacao_top_5
    ]
})

kpis.to_csv(
    "data/analytics/kpis.csv",
    index=False
)

print("\nKPIs consolidados:")
print(kpis)
