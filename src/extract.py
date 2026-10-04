import pandas as pd


def extrair_dados():
    clientes = pd.read_csv("data/raw/clientes.csv")
    fornecedores = pd.read_csv("data/raw/fornecedores.csv")
    produtos = pd.read_csv("data/raw/produtos.csv")
    vendas = pd.read_csv("data/raw/vendas.csv")
    itens_venda = pd.read_csv("data/raw/itens_venda.csv")
    estoque = pd.read_csv("data/raw/estoque.csv")

    print("Dados extraídos com sucesso!")

    print("clientes:", len(clientes))
    print("fornecedores:", len(fornecedores))
    print("produtos:", len(produtos))
    print("vendas:", len(vendas))
    print("itens_venda:", len(itens_venda))
    print("estoque:", len(estoque))

    return {
        "clientes": clientes,
        "fornecedores": fornecedores,
        "produtos": produtos,
        "vendas": vendas,
        "itens_venda": itens_venda,
        "estoque": estoque,
    }



