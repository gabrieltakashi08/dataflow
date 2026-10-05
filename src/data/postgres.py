import os

import pandas as pd
import psycopg2


def conectar():
    return psycopg2.connect(
        host="localhost",
        database="dataflow",
        user="dataflow_user",
        password=os.environ["DATAFLOW_DB_PASSWORD"],
    )


def carregar_vendas():
    conn = conectar()

    try:
        return pd.read_sql_query(
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
    finally:
        conn.close()


def carregar_itens():
    conn = conectar()

    try:
        return pd.read_sql_query(
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
    finally:
        conn.close()


def carregar_produtos():
    conn = conectar()

    try:
        return pd.read_sql_query(
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
    finally:
        conn.close()


def carregar_estoque():
    conn = conectar()

    try:
        return pd.read_sql_query(
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
