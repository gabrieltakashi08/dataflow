CREATE TABLE clientes (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL,
    cidade VARCHAR(100),
    data_cadastro DATE
);

CREATE TABLE fornecedores (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cidade VARCHAR(100)
);

CREATE TABLE produtos (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    preco NUMERIC(12,2) NOT NULL CHECK (preco >= 0),
    fornecedores_id INTEGER REFERENCES fornecedores(id)
);

CREATE TABLE vendas (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id),
    data_venda DATE NOT NULL,
    valor_total NUMERIC(12,2) NOT NULL CHECK (valor_total >= 0)
);

CREATE TABLE itens_venda (
    id INTEGER PRIMARY KEY,
    vendas_id INTEGER NOT NULL REFERENCES vendas(id),
    produto_id INTEGER NOT NULL REFERENCES produtos(id),
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    preco_uni NUMERIC(12,2) NOT NULL CHECK (preco_uni >= 0)
);

CREATE TABLE estoque (
    id INTEGER PRIMARY KEY,
    produto_id INTEGER NOT NULL REFERENCES produtos(id),
    quantidade INTEGER NOT NULL CHECK (quantidade >= 0),
    estoque_min INTEGER NOT NULL CHECK (estoque_min >= 0)
);
