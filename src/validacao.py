import pandas as pd


COLUNAS_VENDAS_CLIENTES = [
    "ID",
    "cliente ID",
    "data venda",
    "valor total",
    "ano",
    "mes",
    "mes_ano",
    "nome",
    "e-mail",
    "cidade",
    "data_cadastro",
]


def validar_vendas_clientes(df):

    for coluna in COLUNAS_VENDAS_CLIENTES:
        assert coluna in df.columns, f"Coluna obrigatória ausente: {coluna}"

    assert df.isnull().sum().sum() == 0, \
        "Existem valores nulos"

    assert df.duplicated().sum() == 0, \
        "Existem registros duplicados"

    assert (df["valor total"] > 0).all(), \
        "Existem valores de venda menores ou iguais a zero"

    assert pd.to_datetime(
        df["data venda"],
        errors="coerce"
    ).notna().all(), \
        "Existem datas de venda inválidas"

    assert df["ID"].notna().all(), \
        "Existem IDs de venda nulos"

    assert df["cliente ID"].notna().all(), \
        "Existem IDs de cliente nulos"

    return True