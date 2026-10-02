import pandas as pd

clientes = pd.read_csv("data/raw/clientes.csv")
fornecedores = pd.read_csv("data/raw/fornecedores.csv")
produtos = pd.read_csv("data/raw/produtos.csv")
vendas = pd.read_csv("data/raw/vendas.csv")
itens_venda = pd.read_csv("data/raw/itens_venda.csv")
estoque = pd.read_csv("data/raw/estoque.csv")

print("clientes:", len(clientes))
print("fornecedores:", len(fornecedores))
print("produtos:", len(produtos))
print("vendas:", len(vendas))
print("itens_venda:", len(itens_venda))
print("estoque:", len(estoque))

print("\n--- clientes ---")
print(clientes.info())

print("\n--- fornecedores ---")
print(fornecedores.info())

print("\n--- produtos ---")
print(produtos.info())

print("\n--- vendas ---")
print(vendas.info())

print("\n--- itens_venda ---")
print(itens_venda.info())

print("\n--- estoque ---")
print(estoque.info())

print("\n--- valores nulos ---")
print("clientes")
print(clientes.isnull() .sum())
print("\nfornecedores")
print(fornecedores.isnull() .sum())
print("\nprodutos")
print(produtos.isnull() .sum())
print("\nvendas")
print(vendas.isnull() .sum())
print("\nitens_venda")
print(itens_venda.isnull() .sum())
print("\nestoque")
print(estoque.isnull() .sum()) 

print("\n--- duplicatas ---")
print("clientes", clientes.duplicated() .sum())
print("fornecedores", fornecedores.duplicated() .sum())
print("produtos", produtos.duplicated() .sum())
print("vendas", vendas.duplicated() .sum())
print("itens_venda", itens_venda.duplicated() .sum())
print("estoque", estoque.duplicated() .sum())

print("\n--- verificação das colunas ---")
print("clientes:", clientes.columns.tolist())
print("fornecedores:", fornecedores.columns.tolist())
print("produtos:", produtos.columns.tolist())
print("vendas:", vendas.columns.tolist())
print("itens_venda:", itens_venda.columns.tolist())
print("estoque", estoque.columns.tolist())

print("\n--- verificação dos IDs ---")
print("IDs de clientes duplicados", clientes["ID"].duplicated() .sum())
print("IDs de fornecedores duplicados", fornecedores["ID"].duplicated() .sum())
print("IDs de produtos duplicados", produtos["ID"].duplicated() .sum())
print("IDs de vendas duplicadas", vendas["ID"].duplicated() .sum())
print("IDs de itens_venda duplicadas", itens_venda["ID"].duplicated() .sum())
print("IDs de estoque", estoque["ID"].duplicated() .sum())

print("\n--- verificação dos relacionamentos ---")
print("clientes inexistentes em vendas:", (~vendas["cliente ID"].isin(clientes["ID"])).sum())
print("fornecedores inexistentes em produtos:", (~produtos["fornecedor ID"].isin(fornecedores["ID"])).sum())
print("produtos inexistentes em itens_venda:", (~itens_venda["produto ID"].isin(produtos["ID"])).sum())
print("vendas inexistentes em itens_venda:", (~itens_venda["venda ID"].isin(vendas["ID"])).sum())
print("produtos inexistentes em estoque:", (~estoque["product ID"].isin(produtos["ID"])).sum())

print("\n--- tipo de dados ---")
print(clientes.dtypes)
print("\n---------------------")
print(fornecedores.dtypes)
print("\n---------------------")
print(produtos.dtypes)
print("\n---------------------")
print(vendas.dtypes)
print("\n---------------------")
print(itens_venda.dtypes)
print("\n---------------------")
print(estoque.dtypes)
print("\n---------------------")

print("\n--- correção datas ---")
print(clientes["data_cadastro"].head())
print(vendas["data venda"].head())



