import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
import streamlit as st


from src.ai.analyst import analisar
from src.ai.context import construir_contexto
# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="DataFlow Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONEXÃO POSTGRESQL
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]


def conectar():
    return psycopg2.connect(
        host="localhost",
        database="dataflow",
        user="dataflow_user",
        password=os.environ["DATAFLOW_DB_PASSWORD"],
    )


# ============================================================
# ESTILO
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        color: #777;
        font-size: 1rem;
        margin-bottom: 1rem;
    }

    div[data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,0.2);
        border-radius: 12px;
        padding: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================

@st.cache_data(ttl=60)
def carregar_dados():

    conn = conectar()

    try:

        vendas = pd.read_sql_query(
            """
            SELECT
                v.id AS venda_id,
                v.cliente_id,
                v.data_venda,
                v.valor_total,
                c.nome AS cliente,
                c.cidade
            FROM vendas v
            JOIN clientes c
                ON c.id = v.cliente_id
            ORDER BY v.data_venda;
            """,
            conn,
        )

        itens = pd.read_sql_query(
            """
            SELECT
                iv.id AS item_id,
                iv.vendas_id AS venda_id,
                iv.produto_id,
                iv.quantidade,
                iv.preco_uni,
                p.nome AS produto,
                p.categoria,
                p.preco AS preco_cadastro
            FROM itens_venda iv
            JOIN produtos p
                ON p.id = iv.produto_id;
            """,
            conn,
        )

        produtos = pd.read_sql_query(
            """
            SELECT
                p.id,
                p.nome,
                p.categoria,
                p.preco,
                p.fornecedores_id,
                f.nome AS fornecedor
            FROM produtos p
            LEFT JOIN fornecedores f
                ON f.id = p.fornecedores_id
            ORDER BY p.nome;
            """,
            conn,
        )

        estoque = pd.read_sql_query(
            """
            SELECT
                e.produto_id,
                e.quantidade,
                e.estoque_min,
                p.nome AS produto,
                p.categoria
            FROM estoque e
            JOIN produtos p
                ON p.id = e.produto_id;
            """,
            conn,
        )

    finally:
        conn.close()

    vendas["data_venda"] = pd.to_datetime(
        vendas["data_venda"],
        errors="coerce",
    )

    vendas["valor_total"] = pd.to_numeric(
        vendas["valor_total"],
        errors="coerce",
    ).fillna(0)

    itens["quantidade"] = pd.to_numeric(
        itens["quantidade"],
        errors="coerce",
    ).fillna(0)

    itens["preco_uni"] = pd.to_numeric(
        itens["preco_uni"],
        errors="coerce",
    ).fillna(0)

    itens["receita_item"] = (
        itens["quantidade"] * itens["preco_uni"]
    )

    estoque["quantidade"] = pd.to_numeric(
        estoque["quantidade"],
        errors="coerce",
    ).fillna(0)

    estoque["estoque_min"] = pd.to_numeric(
        estoque["estoque_min"],
        errors="coerce",
    ).fillna(0)

    return vendas, itens, produtos, estoque


# ============================================================
# CARREGAR
# ============================================================

try:

    vendas, itens, produtos, estoque = carregar_dados()

except Exception as erro:

    st.error("Erro ao conectar ao PostgreSQL.")

    st.code(str(erro))

    st.info(
        "Verifique se DATAFLOW_DB_PASSWORD está configurada "
        "no terminal que iniciou o Streamlit."
    )

    st.stop()


# ============================================================
# VALIDAÇÃO
# ============================================================

if vendas.empty:

    st.error("O PostgreSQL não possui registros na tabela vendas.")

    st.stop()


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    '<div class="main-title">📊 DataFlow Analytics</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Enterprise Sales Data Platform • PostgreSQL • SQL • Pandas • Plotly • Streamlit"
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎛️ DataFlow Control")

st.sidebar.caption(
    "Explore o desempenho comercial usando os filtros abaixo."
)


# ============================================================
# FILTROS
# ============================================================

meses = sorted(
    vendas["data_venda"]
    .dropna()
    .dt.to_period("M")
    .astype(str)
    .unique()
    .tolist()
)

mes_selecionado = st.sidebar.selectbox(
    "📅 Período",
    ["Todos"] + meses,
)


clientes = sorted(
    vendas["cliente"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

cliente_selecionado = st.sidebar.selectbox(
    "👤 Cliente",
    ["Todos"] + clientes,
)


cidades = sorted(
    vendas["cidade"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

cidade_selecionada = st.sidebar.selectbox(
    "🌎 Cidade",
    ["Todas"] + cidades,
)


categorias = sorted(
    itens["categoria"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

categoria_selecionada = st.sidebar.selectbox(
    "📦 Categoria",
    ["Todas"] + categorias,
)


limite_ranking = st.sidebar.slider(
    "Quantidade no ranking",
    min_value=5,
    max_value=20,
    value=10,
)


# ============================================================
# FILTRO DE VENDAS
# ============================================================

vendas_filtradas = vendas.copy()


if mes_selecionado != "Todos":

    vendas_filtradas = vendas_filtradas[
        vendas_filtradas["data_venda"]
        .dt.to_period("M")
        .astype(str)
        == mes_selecionado
    ]


if cliente_selecionado != "Todos":

    vendas_filtradas = vendas_filtradas[
        vendas_filtradas["cliente"]
        == cliente_selecionado
    ]


if cidade_selecionada != "Todas":

    vendas_filtradas = vendas_filtradas[
        vendas_filtradas["cidade"]
        == cidade_selecionada
    ]


# ============================================================
# FILTRO DOS ITENS
# ============================================================

ids_vendas = vendas_filtradas["venda_id"].tolist()


itens_filtrados = itens[
    itens["venda_id"].isin(ids_vendas)
].copy()


if categoria_selecionada != "Todas":

    itens_filtrados = itens_filtrados[
        itens_filtrados["categoria"]
        == categoria_selecionada
    ].copy()


# ============================================================
# MÉTRICAS
# ============================================================

faturamento = vendas_filtradas["valor_total"].sum()

numero_vendas = len(vendas_filtradas)

ticket_medio = (
    faturamento / numero_vendas
    if numero_vendas > 0
    else 0
)

clientes_ativos = vendas_filtradas["cliente"].nunique()

itens_vendidos = itens_filtrados["quantidade"].sum()

produtos_vendidos = itens_filtrados["produto"].nunique()

media_itens_venda = (
    itens_vendidos / numero_vendas
    if numero_vendas > 0
    else 0
)

compras_por_cliente = (
    vendas_filtradas
    .groupby("cliente")
    .size()
)

clientes_recorrentes = int(
    (compras_por_cliente > 1).sum()
)

ranking_cliente_total = (
    vendas_filtradas
    .groupby("cliente")["valor_total"]
    .sum()
    .sort_values(ascending=False)
)

top5_faturamento = ranking_cliente_total.head(5).sum()

participacao_top5 = (
    (top5_faturamento / faturamento) * 100
    if faturamento > 0
    else 0
)

maior_cliente = (
    ranking_cliente_total.index[0]
    if not ranking_cliente_total.empty
    else "-"
)


# ============================================================
# KPIs
# ============================================================

st.subheader("📌 Visão executiva")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Faturamento",
    f"R$ {faturamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
)

col2.metric(
    "Vendas",
    f"{numero_vendas:,}".replace(",", "."),
)

col3.metric(
    "Ticket médio",
    f"R$ {ticket_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
)

col4.metric(
    "Clientes ativos",
    f"{clientes_ativos}",
)


col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Itens vendidos",
    f"{int(itens_vendidos)}",
)

col6.metric(
    "Produtos vendidos",
    f"{produtos_vendidos}",
)

col7.metric(
    "Clientes recorrentes",
    f"{clientes_recorrentes}",
)

col8.metric(
    "Participação Top 5",
    f"{participacao_top5:.1f}%",
)


st.caption(
    f"Maior cliente no período filtrado: **{maior_cliente}**"
)


# ============================================================
# ABAS
# ============================================================

aba1, aba2, aba3, aba4, aba5, aba6 = st.tabs(
    [
        "📊 Visão Geral",
        "👥 Clientes",
        "📦 Produtos",
        "🧾 Vendas",
        "📈 Análises",
        "🤖 AI Analyst",
    ]
)


# ============================================================
# ABA 1 — VISÃO GERAL
# ============================================================

with aba1:

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Evolução do faturamento")

        mensal = (
            vendas_filtradas
            .assign(
                mes=vendas_filtradas["data_venda"]
                .dt.to_period("M")
                .astype(str)
            )
            .groupby("mes", as_index=False)
            .agg(
                faturamento=("valor_total", "sum"),
                vendas=("venda_id", "count"),
            )
        )

        if not mensal.empty:

            fig = px.line(
                mensal,
                x="mes",
                y="faturamento",
                markers=True,
                labels={
                    "mes": "Mês",
                    "faturamento": "Faturamento (R$)",
                },
            )

            fig.update_layout(
                hovermode="x unified",
                height=400,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

    with col2:

        st.subheader("Vendas por cidade")

        cidade_df = (
            vendas_filtradas
            .groupby("cidade", as_index=False)
            .agg(
                faturamento=("valor_total", "sum"),
                vendas=("venda_id", "count"),
            )
            .sort_values(
                "faturamento",
                ascending=False,
            )
            .head(limite_ranking)
        )

        if not cidade_df.empty:

            fig = px.bar(
                cidade_df,
                x="faturamento",
                y="cidade",
                orientation="h",
                text_auto=".2f",
                labels={
                    "faturamento": "Faturamento (R$)",
                    "cidade": "Cidade",
                },
            )

            fig.update_layout(
                height=400,
                yaxis={"categoryorder": "total ascending"},
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )


    st.subheader("Distribuição do faturamento")

    if not ranking_cliente_total.empty:

        fig = px.bar(
            ranking_cliente_total
            .head(limite_ranking)
            .reset_index()
            .rename(columns={"valor_total": "faturamento"}),
            x="faturamento",
            y="cliente",
            orientation="h",
            text_auto=".2f",
            labels={
                "faturamento": "Faturamento (R$)",
                "cliente": "Cliente",
            },
        )

        fig.update_layout(
            height=450,
            yaxis={"categoryorder": "total ascending"},
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )


# ============================================================
# ABA 2 — CLIENTES
# ============================================================

with aba2:

    st.subheader("Ranking de clientes")

    clientes_df = (
        vendas_filtradas
        .groupby("cliente", as_index=False)
        .agg(
            faturamento=("valor_total", "sum"),
            compras=("venda_id", "count"),
            ticket_medio=("valor_total", "mean"),
        )
        .sort_values(
            "faturamento",
            ascending=False,
        )
    )

    if not clientes_df.empty:

        clientes_df["participacao_%"] = (
            clientes_df["faturamento"]
            / faturamento
            * 100
            if faturamento > 0
            else 0
        )

        st.dataframe(
            clientes_df,
            use_container_width=True,
            hide_index=True,
        )

        fig = px.bar(
            clientes_df.head(limite_ranking),
            x="faturamento",
            y="cliente",
            orientation="h",
            text_auto=".2f",
        )

        fig.update_layout(
            height=450,
            yaxis={"categoryorder": "total ascending"},
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )


# ============================================================
# ABA 3 — PRODUTOS
# ============================================================

with aba3:

    st.subheader("Performance dos produtos")

    produtos_df = (
        itens_filtrados
        .groupby(
            ["produto", "categoria"],
            as_index=False,
        )
        .agg(
            quantidade=("quantidade", "sum"),
            receita=("receita_item", "sum"),
        )
        .sort_values(
            "receita",
            ascending=False,
        )
    )

    if not produtos_df.empty:

        col1, col2 = st.columns(2)

        with col1:

            fig = px.bar(
                produtos_df.head(limite_ranking),
                x="receita",
                y="produto",
                color="categoria",
                orientation="h",
                text_auto=".2f",
            )

            fig.update_layout(
                height=500,
                yaxis={"categoryorder": "total ascending"},
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        with col2:

            categoria_df = (
                produtos_df
                .groupby("categoria", as_index=False)
                .agg(
                    receita=("receita", "sum"),
                    quantidade=("quantidade", "sum"),
                )
                .sort_values(
                    "receita",
                    ascending=False,
                )
            )

            fig = px.pie(
                categoria_df,
                names="categoria",
                values="receita",
                hole=0.45,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        st.dataframe(
            produtos_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "Nenhum produto encontrado com os filtros atuais."
        )


# ============================================================
# ABA 4 — VENDAS
# ============================================================

with aba4:

    st.subheader("Transações")

    vendas_exibicao = vendas_filtradas.copy()

    vendas_exibicao["data_venda"] = (
        vendas_exibicao["data_venda"]
        .dt.strftime("%d/%m/%Y")
    )

    vendas_exibicao = vendas_exibicao.rename(
        columns={
            "venda_id": "ID venda",
            "data_venda": "Data",
            "cliente": "Cliente",
            "cidade": "Cidade",
            "valor_total": "Valor",
        }
    )

    colunas = [
        "ID venda",
        "Data",
        "Cliente",
        "Cidade",
        "Valor",
    ]

    st.dataframe(
        vendas_exibicao[colunas],
        use_container_width=True,
        hide_index=True,
    )

    csv = vendas_exibicao[colunas].to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Baixar vendas filtradas",
        data=csv,
        file_name="dataflow_vendas_filtradas.csv",
        mime="text/csv",
    )


# ============================================================
# ABA 5 — ANÁLISES
# ============================================================

with aba5:

    st.subheader("🔎 Análises de negócio")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Média de itens por venda",
            f"{media_itens_venda:.2f}",
        )

    with col2:

        if not vendas_filtradas.empty:

            maior_venda = vendas_filtradas[
                "valor_total"
            ].max()

        else:

            maior_venda = 0

        st.metric(
            "Maior venda",
            f"R$ {maior_venda:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        )

    with col3:

        if not vendas_filtradas.empty:

            menor_venda = vendas_filtradas[
                "valor_total"
            ].min()

        else:

            menor_venda = 0

        st.metric(
            "Menor venda",
            f"R$ {menor_venda:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        )


    st.divider()

    st.subheader("Estoque")

    estoque_analise = estoque.copy()

    estoque_analise["status"] = estoque_analise.apply(
        lambda row:
        "⚠️ Reposição"
        if row["quantidade"] <= row["estoque_min"]
        else "✅ Normal",
        axis=1,
    )

    estoque_analise = estoque_analise.sort_values(
        "quantidade"
    )

    st.dataframe(
        estoque_analise[
            [
                "produto",
                "categoria",
                "quantidade",
                "estoque_min",
                "status",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


    st.divider()

    st.subheader("Crescimento mensal")

    crescimento = (
        vendas
        .assign(
            mes=vendas["data_venda"]
            .dt.to_period("M")
            .astype(str)
        )
        .groupby("mes", as_index=False)
        .agg(
            faturamento=("valor_total", "sum")
        )
        .sort_values("mes")
    )

    crescimento["crescimento_%"] = (
        crescimento["faturamento"]
        .pct_change()
        * 100
    )

    crescimento["crescimento_%"] = (
        crescimento["crescimento_%"]
        .round(2)
    )

    st.dataframe(
        crescimento,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# ABA 6 — AI ANALYST
# ============================================================

with aba6:

    st.subheader("🤖 DataFlow AI Analyst")

    st.markdown(
        """
        Pergunte sobre os dados do DataFlow em linguagem natural.
        A análise é baseada nos dados disponíveis na plataforma.
        """
    )

    pergunta = st.text_area(
        "Faça uma pergunta",
        placeholder=(
            "Ex.: Qual foi o mês de maior faturamento? "
            "Quais clientes mais geraram receita?"
        ),
        height=100,
    )

    analisar_btn = st.button(
        "🔎 Analisar",
        type="primary",
    )

    if analisar_btn:

        if not pergunta.strip():

            st.warning("Digite uma pergunta antes de analisar.")

        else:

            with st.spinner("Analisando os dados..."):

                contexto = construir_contexto()

                try:

                    resposta = analisar(
                        pergunta,
                        contexto,
                    )

                    st.markdown("### 💡 Análise")

                    st.write(resposta)

                except Exception as e:

                    st.error(
                        f"Não foi possível realizar a análise: {e}"
                    )



# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "DataFlow Analytics • PostgreSQL • SQL • Pandas • Plotly • Streamlit"
)
