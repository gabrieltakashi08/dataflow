CREATE TABLE clientes(id INTEGER PRIMARY KEY, nome TEXT NOT NULL, email TEXT NOT NULL, cidade TEXT, data_cadastro DATE);
CREATE TABLE fornecedores(id INTEGER PRIMARY KEY, nome TEXT NOT NULL, cidade TEXT);
CREATE TABLE produtos(id INTEGER PRIMARY KEY, nome TEXT NOT NULL, categoria TEXT NOT NULL, preco REAL NOT NULL, fornecedores_id INTEGER, FOREIGN KEY (fornecedores_id) REFERENCES fornecedores(id));
CREATE TABLE vendas(id INTEGER PRIMARY KEY, cliente_id INTEGER, FOREIGN KEY (clientes_id) REFERENCES clientes(id), data_venda DATE, valor_total REAL NOT NULL);
CREATE TABLE itens_vendas(id INTEGER PRIMARY KEY, vendas_id INTEGER, FOREIGN KEY (vendas_id) REFERENCES vendas(id), produtos_id INTEGER, FOREIGN KEY (produtos_id) REFERENCES produtos(id), quantidade INTEGER NOTNULL, preco_uni REAL NOT NULL);
CREATE TABLE estoque(id INTEGER PRIMARY KEY, produto_id INTEGER, FOREIGN KEY (produto_id) REFERENCES produtos(id), quantidade INTEGER NOT NULL, estoque_min INTEGER NOTNULL);
CREATE TABLE itens_vendas_nova((id INTEGER PRIMARY KEY, vendas_id INTEGER, FOREIGN KEY (vendas_id) REFERENCES vendas(id), produtos_id INTEGER, FOREIGN KEY (produtos_id) REFERENCES produtos(id), quantidade INTEGER NOTNULL, preco_uni REAL NOT NULL);
