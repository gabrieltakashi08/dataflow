import pandas as pd
from pathlib import Path

from src.validacao import validar_vendas_clientes


BASE_DIR = Path(__file__).resolve().parents[1]


def test_vendas_clientes_existe():
    arquivo = BASE_DIR / "data/processed/vendas_clientes.csv"

    assert arquivo.exists()


def test_vendas_clientes_sem_valores_nulos():
    arquivo = BASE_DIR / "data/processed/vendas_clientes.csv"

    df = pd.read_csv(arquivo)

    assert df.isnull().sum().sum() == 0


def test_vendas_clientes_sem_duplicatas():
    arquivo = BASE_DIR / "data/processed/vendas_clientes.csv"

    df = pd.read_csv(arquivo)

    assert df.duplicated().sum() == 0


def test_quantidade_de_vendas():
    arquivo = BASE_DIR / "data/processed/vendas_clientes.csv"

    df = pd.read_csv(arquivo)

    assert len(df) == 50


def test_valores_de_venda_positivos():
    arquivo = BASE_DIR / "data/processed/vendas_clientes.csv"

    df = pd.read_csv(arquivo)

    assert (df["valor total"] > 0).all()


def test_kpis_existe():
    arquivo = BASE_DIR / "data/analytics/kpis.csv"

    assert arquivo.exists()


def test_datasets_analiticos_existem():

    arquivos = [
        "data/analytics/clientes_analytics.csv",
        "data/analytics/mensal_analytics.csv",
        "data/analytics/cidade_analytics.csv",
    ]

    for arquivo in arquivos:
        assert (BASE_DIR / arquivo).exists()


def test_validacao_completa_vendas_clientes():

    arquivo = BASE_DIR / "data/processed/vendas_clientes.csv"

    df = pd.read_csv(arquivo)

    assert validar_vendas_clientes(df) is True