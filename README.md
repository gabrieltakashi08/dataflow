# DataFlow — Enterprise Sales Data Platform

Pipeline de dados desenvolvido em Python para extração, transformação, validação, armazenamento, análise e visualização de dados de vendas.

O projeto foi desenvolvido com foco em práticas de Engenharia de Dados, incluindo modularização, qualidade de dados, SQL analítico, PostgreSQL, testes automatizados e integração contínua.

## Objetivo

O DataFlow simula uma plataforma de dados de vendas, partindo de arquivos CSV brutos e produzindo dados processados, datasets analíticos, indicadores de negócio e visualizações.

O pipeline integra as principais etapas:

CSV Brutos → Extract → Transform → Validação → PostgreSQL → Análise SQL/Python → Datasets Analíticos → Dashboard

O projeto também possui CI com GitHub Actions para execução automatizada do pipeline e dos testes.

## Arquitetura

data/raw/
    ↓
src/extract.py
    ↓
src/transform.py
    ↓
src/validacao.py
    ↓
PostgreSQL
    ↓
src/analise.py
    ↓
data/analytics/
    ↓
Dashboard / Visualizações

## Estrutura do Projeto

dataflow/
├── data/
│   ├── raw/
│   ├── processed/
│   └── analytics/
├── database/
│   └── vendas.db
├── sql/
│   └── schema.sql
├── src/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   ├── validacao.py
│   ├── analise.py
│   ├── load_postgres.py
│   ├── pipeline.py
│   ├── dashboard/
│   │   └── dashboard.py
│   └── visualizacoes/
│       ├── __init__.py
│       └── graficos.py
├── tests/
│   ├── __init__.py
│   └── test_data_quality.py
├── .github/
│   └── workflows/
│       └── dataflow.yml
├── .gitignore
├── requirements.txt
└── README.md

## Pipeline

### 1. Extract

Leitura dos dados brutos utilizando Pandas:

- Clientes
- Fornecedores
- Produtos
- Vendas
- Itens de venda
- Estoque

### 2. Transform

Principais transformações:

- Conversão e tratamento de datas
- Criação de ano, mês e período mensal
- Tratamento de valores numéricos
- Integração entre vendas e clientes
- Geração do dataset vendas_clientes.csv
- Preparação dos dados para análise

### 3. Validação

O pipeline executa validações de qualidade antes das etapas analíticas:

- Colunas obrigatórias
- Valores nulos
- Registros duplicados
- Valores de venda inválidos
- Datas inválidas
- IDs de venda
- IDs de cliente

### 4. PostgreSQL

Os dados brutos são carregados em um banco PostgreSQL utilizando psycopg2.

O modelo possui seis tabelas:

- clientes
- fornecedores
- produtos
- vendas
- itens_venda
- estoque

As tabelas utilizam chaves primárias, chaves estrangeiras e restrições de integridade.

Também foram utilizados índices em colunas relacionadas a chaves estrangeiras e consultas analíticas.

### 5. Análise

O projeto gera datasets analíticos para diferentes dimensões do negócio.

#### Clientes

- Faturamento por cliente
- Quantidade de compras
- Ticket médio
- Participação no faturamento
- Ranking de clientes

#### Vendas

- Faturamento total
- Quantidade de vendas
- Maior venda
- Menor venda
- Mediana
- Desvio padrão
- Ticket médio

#### Análise temporal

- Faturamento mensal
- Crescimento mensal
- Faturamento acumulado
- Quantidade de vendas por mês
- Ticket médio mensal

#### Geografia

- Faturamento por cidade
- Quantidade de vendas por cidade
- Ticket médio por cidade
- Participação das cidades no faturamento

#### Produtos e categorias

- Faturamento por produto
- Produtos mais vendidos
- Faturamento por categoria
- Ranking de produtos por categoria
- Produto campeão por categoria

## SQL Analytics

A camada PostgreSQL também foi utilizada para consultas analíticas, incluindo:

- JOIN
- GROUP BY
- CTEs
- Funções de janela
- RANK()
- ROW_NUMBER()
- LAG()
- Agregações
- Análise temporal
- Análise por categoria
- Análise de estoque

Também foram realizados testes com EXPLAIN ANALYZE e criação de índices para avaliar o comportamento do PostgreSQL.

## Dashboard e Visualizações

As visualizações são geradas utilizando Matplotlib:

- Evolução do faturamento mensal
- Top 10 clientes
- Top 10 cidades
- Ticket médio mensal
- Faturamento mensal
- Faturamento por cidade
- Ticket médio por cidade

## Indicadores Atuais

Dataset atual:

- 50 vendas
- 20 clientes
- 20 cidades
- R$ 8.803,30 de faturamento total
- R$ 176,07 de ticket médio
- R$ 512,70 de maior venda
- R$ 42,90 de menor venda
- R$ 145,95 de mediana
- R$ 111,68 de desvio padrão
- 50,02% de crescimento entre o primeiro e o último mês analisado
- 44,04% do faturamento concentrado nos 5 maiores clientes

## Qualidade e Testes

O projeto utiliza Pytest para testes automatizados de qualidade dos dados.

Os testes verificam:

- Existência dos arquivos processados
- Ausência de valores nulos
- Ausência de registros duplicados
- Quantidade esperada de vendas
- Valores de venda positivos
- Existência dos KPIs
- Existência dos datasets analíticos
- Execução da validação completa do dataset

Resultado atual:

8 passed

## Integração Contínua

O projeto utiliza GitHub Actions para automatizar a execução do pipeline e dos testes.

O workflow realiza:

1. Checkout do código
2. Configuração do Python 3.11
3. Instalação das dependências
4. Inicialização do PostgreSQL
5. Criação do schema
6. Execução do pipeline
7. Execução dos testes

## Tecnologias

- Python 3.11
- Pandas
- Matplotlib
- PostgreSQL
- psycopg2
- SQLite
- SQL
- Pytest
- Git
- GitHub Actions

## Como Executar

Clone o repositório:

git clone git@github.com:gabrieltakashi08/dataflow.git
cd dataflow

Crie e ative o ambiente virtual:

python3 -m venv .venv
source .venv/bin/activate

Instale as dependências:

pip install -r requirements.txt

Configure a variável de ambiente utilizada pelo PostgreSQL:

export DATAFLOW_DB_PASSWORD="sua_senha"

Execute o pipeline:

python -m src.pipeline

Execute os testes:

python -m pytest -v

## Resultados

O pipeline gera automaticamente:

data/processed/
- vendas_clientes.csv
- faturamento_mensal.png
- faturamento_cidade.png
- ticket_medio_cidade.png

data/analytics/
- clientes_analytics.csv
- mensal_analytics.csv
- cidade_analytics.csv
- kpis.csv
- evolucao_faturamento.png
- top_clientes.png
- top_cidades.png
- ticket_medio_mensal.png

## Próximos Passos

- Dashboard interativo
- Maior cobertura de testes
- Melhorias de observabilidade e logging
- Containerização com Docker
- Orquestração do pipeline
- Evolução da arquitetura para um ambiente mais próximo de produção