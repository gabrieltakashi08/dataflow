import pandas as pd

from src.analytics.queries import (
    faturamento_por_mes,
    ranking_clientes,
    pareto_clientes,
    crescimento_mensal,
    produtos_ranking,
    estoque_critico,
    faturamento_produto_mes,
    faturamento_categoria_mes,
    faturamento_cliente_mes,
    contribuicao_crescimento_mensal,
)


def obter_faturamento_mensal():
    dados = faturamento_por_mes()

    return pd.DataFrame(
        dados,
        columns=[
            "mes",
            "faturamento",
            "quantidade_vendas",
            "ticket_medio",
        ],
    )


def obter_ranking_clientes():
    dados = ranking_clientes()

    return pd.DataFrame(
        dados,
        columns=[
            "cliente",
            "faturamento",
            "quantidade_compras",
            "ticket_medio",
            "ranking",
        ],
    )


def obter_pareto_clientes():
    dados = pareto_clientes()

    return pd.DataFrame(
        dados,
        columns=[
            "cliente",
            "faturamento",
            "percentual_acumulado",
        ],
    )


def obter_crescimento_mensal():
    dados = crescimento_mensal()

    return pd.DataFrame(
        dados,
        columns=[
            "mes",
            "faturamento",
            "faturamento_anterior",
            "crescimento_percentual",
        ],
    )


def obter_ranking_produtos():
    dados = produtos_ranking()

    return pd.DataFrame(
        dados,
        columns=[
            "produto",
            "categoria",
            "quantidade_vendida",
            "receita",
            "ranking",
        ],
    )


def obter_estoque_critico():
    dados = estoque_critico()

    return pd.DataFrame(
        dados,
        columns=[
            "produto",
            "categoria",
            "quantidade",
            "estoque_min",
            "status",
        ],
    )


def obter_faturamento_produto_mes():
    dados = faturamento_produto_mes()

    return pd.DataFrame(
        dados,
        columns=[
            "mes",
            "produto",
            "categoria",
            "receita",
            "quantidade_vendida",
        ],
    )


def obter_faturamento_categoria_mes():
    dados = faturamento_categoria_mes()

    return pd.DataFrame(
        dados,
        columns=[
            "mes",
            "categoria",
            "receita",
            "quantidade_vendida",
        ],
    )


def obter_faturamento_cliente_mes():
    dados = faturamento_cliente_mes()

    return pd.DataFrame(
        dados,
        columns=[
            "mes",
            "cliente",
            "faturamento",
            "quantidade_compras",
            "ticket_medio",
        ],
    )


def obter_contribuicao_crescimento_mensal():
    dados = contribuicao_crescimento_mensal()

    return pd.DataFrame(
        dados,
        columns=[
            "mes",
            "faturamento",
            "faturamento_anterior",
            "variacao_absoluta",
            "variacao_percentual",
        ],
    )
