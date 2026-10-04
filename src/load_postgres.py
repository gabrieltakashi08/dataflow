import os
from pathlib import Path

import pandas as pd
import psycopg2


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"


def conectar():
    return psycopg2.connect(
        host="localhost",
        database="dataflow",
        user="dataflow_user",
        password=os.environ["DATAFLOW_DB_PASSWORD"],
    )


def carregar():
    clientes = pd.read_csv(RAW_DIR / "clientes.csv")
    fornecedores = pd.read_csv(RAW_DIR / "fornecedores.csv")
    produtos = pd.read_csv(RAW_DIR / "produtos.csv")
    vendas = pd.read_csv(RAW_DIR / "vendas.csv")
    itens_venda = pd.read_csv(RAW_DIR / "itens_venda.csv")
    estoque = pd.read_csv(RAW_DIR / "estoque.csv")

    conn = conectar()

    try:
        with conn.cursor() as cur:

            for _, row in clientes.iterrows():
                cur.execute(
                    """
                    INSERT INTO clientes
                        (id, nome, email, cidade, data_cadastro)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                    """,
                    (
                        int(row["ID"]),
                        row["nome"],
                        row["e-mail"],
                        row["cidade"],
                        row["data_cadastro"],
                    ),
                )

            for _, row in fornecedores.iterrows():
                cur.execute(
                    """
                    INSERT INTO fornecedores
                        (id, nome, cidade)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                    """,
                    (
                        int(row["ID"]),
                        row["nome"],
                        row["cidade"],
                    ),
                )

            for _, row in produtos.iterrows():
                cur.execute(
                    """
                    INSERT INTO produtos
                        (id, nome, categoria, preco, fornecedores_id)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                    """,
                    (
                        int(row["ID"]),
                        row["nome"],
                        row["categoria"],
                        float(row["preço"]),
                        int(row["fornecedor ID"]),
                    ),
                )

            for _, row in vendas.iterrows():
                cur.execute(
                    """
                    INSERT INTO vendas
                        (id, cliente_id, data_venda, valor_total)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                    """,
                    (
                        int(row["ID"]),
                        int(row["cliente ID"]),
                        row["data venda"],
                        float(row["valor total"]),
                    ),
                )

            for _, row in itens_venda.iterrows():
                cur.execute(
                    """
                    INSERT INTO itens_venda
                        (id, vendas_id, produto_id, quantidade, preco_uni)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                    """,
                    (
                        int(row["ID"]),
                        int(row["venda ID"]),
                        int(row["produto ID"]),
                        int(row["quantidade"]),
                        float(row["preço Uni"]),
                    ),
                )

            for _, row in estoque.iterrows():
                cur.execute(
                    """
                    INSERT INTO estoque
                        (id, produto_id, quantidade, estoque_min)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                    """,
                    (
                        int(row["ID"]),
                        int(row["product ID"]),
                        int(row["quantidade"]),
                        int(row["estoque mínimo"]),
                    ),
                )

        conn.commit()

        print("Carga PostgreSQL concluída com sucesso!")
        print(f"clientes: {len(clientes)}")
        print(f"fornecedores: {len(fornecedores)}")
        print(f"produtos: {len(produtos)}")
        print(f"vendas: {len(vendas)}")
        print(f"itens_venda: {len(itens_venda)}")
        print(f"estoque: {len(estoque)}")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    carregar()
