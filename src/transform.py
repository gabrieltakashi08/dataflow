import pandas as pd

from src.visualizacoes.graficos import (
    grafico_faturamento_mensal,
    grafico_faturamento_cidade,
    grafico_ticket_medio_cidade
)


def transformar_dados(dados):

    clientes = dados["clientes"].copy()
    vendas = dados["vendas"].copy()

    clientes["data_cadastro"] = pd.to_datetime(
        clientes["data_cadastro"]
    )

    vendas["data venda"] = pd.to_datetime(
        vendas["data venda"]
    )

    vendas["ano"] = vendas["data venda"].dt.year
    vendas["mes"] = vendas["data venda"].dt.month
    vendas["mes_ano"] = vendas["data venda"].dt.to_period("M")
    vendas["valor total"] = vendas["valor total"].round(2)

    faturamento_total = vendas["valor total"].sum().round(2)
    faturamento_mensal = (
        vendas
        .groupby("mes_ano")["valor total"]
        .sum()
        .round(2)
        .sort_index()
    )

    maior_venda = vendas["valor total"].max()
    menor_venda = vendas["valor total"].min()
    desvio_padrao = vendas["valor total"].std()
    mediana_venda = vendas["valor total"].median()

    venda_por_mes = vendas.groupby("mes_ano").size()
    media_de_vendas = venda_por_mes.mean()

    faturamento_max_mes = faturamento_mensal.max()
    faturamento_min_mes = faturamento_mensal.min()

    ticket_medio = vendas["valor total"].mean()
    quantidade_vendas = len(vendas)

    crescimento_mensal = faturamento_mensal.pct_change() * 100

    print("\n=== TRANSFORMAÇÃO ===")
    print("Faturamento total:", faturamento_total)
    print("Ticket médio:", round(ticket_medio, 2))
    print("Quantidade de vendas:", quantidade_vendas)
    print("Maior venda:", round(maior_venda, 2))
    print("Menor venda:", round(menor_venda, 2))
    print("Mediana:", round(mediana_venda, 2))
    print("Desvio padrão:", round(desvio_padrao, 2))
    print("Média de vendas por mês:", round(media_de_vendas, 2))
    print("Maior faturamento mensal:", round(faturamento_max_mes, 2))
    print("Menor faturamento mensal:", round(faturamento_min_mes, 2))
    print("Crescimento mensal:")
    print(crescimento_mensal.round(2))

    vendas_clientes = vendas.merge(
        clientes,
        left_on="cliente ID",
        right_on="ID",
        how="left"
    )

    vendas_clientes = vendas_clientes.drop(
        columns=["ID_y"]
    )

    vendas_clientes = vendas_clientes.rename(
        columns={"ID_x": "ID"}
    )

    vendas_clientes.to_csv(
        "data/processed/vendas_clientes.csv",
        index=False
    )

    faturamento_cidade = (
        vendas_clientes
        .groupby("cidade")["valor total"]
        .sum()
        .sort_values(ascending=False)
    )

    ticket_medio_cidade = (
        vendas_clientes
        .groupby("cidade")["valor total"]
        .mean()
        .round(2)
        .sort_values(ascending=False)
    )

    grafico_faturamento_mensal(faturamento_mensal)
    grafico_faturamento_cidade(faturamento_cidade)
    grafico_ticket_medio_cidade(ticket_medio_cidade)

    print("\nDados transformados com sucesso!")
    print("Arquivo gerado:")
    print("data/processed/vendas_clientes.csv")

    return vendas_clientes