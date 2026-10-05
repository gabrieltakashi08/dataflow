from src.analytics.service import (
    obter_faturamento_mensal,
    obter_ranking_clientes,
    obter_pareto_clientes,
    obter_crescimento_mensal,
    obter_ranking_produtos,
    obter_estoque_critico,
    obter_faturamento_produto_mes,
    obter_faturamento_categoria_mes,
    obter_faturamento_cliente_mes,
    obter_contribuicao_crescimento_mensal,
)


def construir_contexto():
    # ============================================================
    # ANALYTICS ENGINE
    # ============================================================

    faturamento = obter_faturamento_mensal()
    clientes = obter_ranking_clientes()
    pareto = obter_pareto_clientes()
    crescimento = obter_crescimento_mensal()
    produtos = obter_ranking_produtos()
    estoque = obter_estoque_critico()

    produto_mes = obter_faturamento_produto_mes()
    categoria_mes = obter_faturamento_categoria_mes()
    cliente_mes = obter_faturamento_cliente_mes()
    contribuicao = obter_contribuicao_crescimento_mensal()

    # ============================================================
    # RESUMO EXECUTIVO
    # ============================================================

    faturamento_total = faturamento["faturamento"].sum()
    quantidade_vendas = faturamento["quantidade_vendas"].sum()

    ticket_medio = (
        faturamento_total / quantidade_vendas
        if quantidade_vendas
        else 0
    )

    melhor_mes = faturamento.loc[
        faturamento["faturamento"].idxmax()
    ]

    pior_mes = faturamento.loc[
        faturamento["faturamento"].idxmin()
    ]

    maior_crescimento = crescimento.loc[
        crescimento["crescimento_percentual"].idxmax()
    ]

    maior_queda = crescimento.loc[
        crescimento["crescimento_percentual"].idxmin()
    ]

    estoque_critico = estoque[
        estoque["status"] == "CRÍTICO"
    ]

    # ============================================================
    # TOP PRODUTOS
    # ============================================================

    top_produtos = produtos.head(10)

    # ============================================================
    # TOP CATEGORIAS
    # ============================================================

    top_categorias = (
        categoria_mes
        .groupby("categoria", as_index=False)["receita"]
        .sum()
        .sort_values("receita", ascending=False)
        .head(10)
    )

    # ============================================================
    # TOP CLIENTES
    # ============================================================

    top_clientes = clientes.head(10)

    # ============================================================
    # PRODUTOS POR MÊS
    # ============================================================

    produto_mes_top = (
        produto_mes
        .sort_values(
            ["mes", "receita"],
            ascending=[True, False],
        )
        .groupby("mes")
        .head(5)
    )

    # ============================================================
    # CATEGORIAS POR MÊS
    # ============================================================

    categoria_mes_top = (
        categoria_mes
        .sort_values(
            ["mes", "receita"],
            ascending=[True, False],
        )
    )

    # ============================================================
    # CLIENTES POR MÊS
    # ============================================================

    cliente_mes_top = (
        cliente_mes
        .sort_values(
            ["mes", "faturamento"],
            ascending=[True, False],
        )
        .groupby("mes")
        .head(5)
    )

    # ============================================================
    # CONTEXTO
    # ============================================================

    contexto = f"""
DATAFLOW AI ANALYST
CONTEXTO ANALÍTICO GERADO PELO ANALYTICS ENGINE

============================================================
1. RESUMO EXECUTIVO
============================================================

Faturamento total:
R$ {faturamento_total:,.2f}

Quantidade total de vendas:
{quantidade_vendas}

Ticket médio geral:
R$ {ticket_medio:,.2f}

Melhor mês:
{melhor_mes["mes"]} — R$ {melhor_mes["faturamento"]:,.2f}

Pior mês:
{pior_mes["mes"]} — R$ {pior_mes["faturamento"]:,.2f}

Maior crescimento mensal:
{maior_crescimento["mes"]} — {maior_crescimento["crescimento_percentual"]:.2f}%

Maior queda mensal:
{maior_queda["mes"]} — {maior_queda["crescimento_percentual"]:.2f}%

Quantidade de produtos com estoque crítico:
{len(estoque_critico)}


============================================================
2. FATURAMENTO MENSAL
============================================================

{faturamento.to_string(index=False)}


============================================================
3. VARIAÇÃO MENSAL
============================================================

{contribuicao.to_string(index=False)}


============================================================
4. RANKING DE CLIENTES
============================================================

{top_clientes.to_string(index=False)}


============================================================
5. PARETO DE CLIENTES
============================================================

{pareto.head(10).to_string(index=False)}


============================================================
6. RANKING DE PRODUTOS
============================================================

{top_produtos.to_string(index=False)}


============================================================
7. RECEITA POR CATEGORIA
============================================================

{top_categorias.to_string(index=False)}


============================================================
8. PRODUTOS POR MÊS — TOP 5
============================================================

{produto_mes_top.to_string(index=False)}


============================================================
9. CATEGORIAS POR MÊS
============================================================

{categoria_mes_top.to_string(index=False)}


============================================================
10. CLIENTES POR MÊS — TOP 5
============================================================

{cliente_mes_top.to_string(index=False)}


============================================================
11. ESTOQUE
============================================================

{estoque.to_string(index=False)}


============================================================
12. REGRAS DE INTERPRETAÇÃO
============================================================

- Os dados acima foram calculados pelo Analytics Engine.
- A IA deve interpretar os resultados, não inventar dados.
- Não assumir causalidade quando os dados apenas mostram correlação.
- Quando possível, comparar períodos usando valores absolutos e percentuais.
- Para explicar crescimento ou queda, considerar:
  faturamento, quantidade de vendas, ticket médio,
  produtos, categorias e clientes.
- Se uma informação não estiver disponível, declarar explicitamente.
- Diferenciar fatos observados de interpretações.
"""

    return contexto
