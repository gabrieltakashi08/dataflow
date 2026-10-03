# DataFlow — Enterprise Sales Data Platform

Pipeline de dados desenvolvido em Python para extração, transformação, validação, análise e visualização de dados de vendas.

## Objetivo

O DataFlow demonstra um fluxo completo de dados, desde dados brutos até datasets analíticos, indicadores de negócio e visualizações.

O projeto foi estruturado com foco em práticas de Engenharia de Dados e Analytics, incluindo modularização, validação de qualidade, testes automatizados e execução integrada por pipeline.

## Arquitetura

```text
Dados Brutos
     ↓
Extract
     ↓
Transform
     ↓
Validação
     ↓
Analysis
     ↓
Datasets Analíticos
     ↓
Dashboard / Visualizações
```

## Estrutura do Projeto

```text
dataflow/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── analytics/
│
├── database/
│   └── vendas.db
│
├── src/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   ├── validacao.py
│   ├── analise.py
│   ├── pipeline.py
│   │
│   ├── dashboard/
│   │   └── dashboard.py
│   │
│   └── visualizacoes/
│       ├── __init__.py
│       └── graficos.py
│
├── tests/
│   ├── __init__.py
│   └── test_data_quality.py
│
├── sql/
│
├── .gitignore
└── README.md
```

## Pipeline

### 1. Extract

Leitura dos dados brutos:

* Clientes
* Fornecedores
* Produtos
* Vendas
* Itens de venda
* Estoque

Os dados são carregados utilizando Pandas.

### 2. Transform

Principais transformações:

* Conversão de datas
* Criação de ano e mês
* Criação do período mensal
* Tratamento de valores numéricos
* Integração entre vendas e clientes
* Cálculo de métricas de negócio
* Geração de dados processados
* Geração de visualizações

O dataset integrado `vendas_clientes.csv` possui 50 registros e 11 colunas.

### 3. Validação

O pipeline possui validações automatizadas para:

* Colunas obrigatórias
* Valores nulos
* Registros duplicados
* Valores de venda inválidos
* Datas inválidas
* IDs de venda
* IDs de cliente

### 4. Analysis

São gerados datasets analíticos para diferentes dimensões do negócio.

#### Clientes

* Faturamento por cliente
* Quantidade de compras
* Ticket médio
* Participação no faturamento
* Top clientes
* Concentração de faturamento

#### Vendas

* Faturamento total
* Quantidade de vendas
* Maior venda
* Menor venda
* Mediana
* Desvio padrão
* Ticket médio

#### Análise temporal

* Faturamento mensal
* Crescimento mensal
* Crescimento entre períodos
* Faturamento acumulado
* Quantidade de vendas por mês
* Ticket médio mensal

#### Geografia

* Faturamento por cidade
* Quantidade de vendas por cidade
* Ticket médio por cidade
* Participação das cidades no faturamento

### 5. Dashboard e Visualizações

O projeto gera visualizações utilizando Matplotlib:

* Evolução do faturamento mensal
* Top 10 clientes
* Top 10 cidades
* Ticket médio mensal
* Faturamento mensal
* Faturamento por cidade
* Ticket médio por cidade

## Datasets Gerados

### Dados processados

```text
data/processed/vendas_clientes.csv
```

### Datasets analíticos

```text
data/analytics/clientes_analytics.csv
data/analytics/mensal_analytics.csv
data/analytics/cidade_analytics.csv
data/analytics/kpis.csv
```

### Visualizações

```text
data/processed/faturamento_mensal.png
data/processed/faturamento_cidade.png
data/processed/ticket_medio_cidade.png

data/analytics/evolucao_faturamento.png
data/analytics/top_clientes.png
data/analytics/top_cidades.png
data/analytics/ticket_medio_mensal.png
```

## Indicadores Atuais

Com o dataset utilizado atualmente:

* 50 vendas
* 20 clientes
* 20 cidades
* R$ 8.803,30 de faturamento total
* R$ 176,07 de ticket médio
* R$ 512,70 de maior venda
* R$ 42,90 de menor venda
* R$ 145,95 de mediana das vendas
* R$ 111,68 de desvio padrão
* 50,02% de crescimento entre o primeiro e o último mês analisado
* 44,04% do faturamento concentrado nos 5 maiores clientes

## Qualidade dos Dados

O projeto possui validações de qualidade e testes automatizados utilizando Pytest.

Resultado atual:

```text
8 passed
```

Os testes verificam:

* Existência dos arquivos processados
* Ausência de valores nulos
* Ausência de registros duplicados
* Quantidade esperada de vendas
* Valores de venda positivos
* Existência dos KPIs
* Existência dos datasets analíticos
* Execução da validação completa do dataset

## Tecnologias

* Python
* Pandas
* Matplotlib
* SQLite
* SQL
* Pytest
* Git

## Execução

Clone o projeto e entre no diretório:

```bash
cd dataflow
```

Ative o ambiente virtual:

```bash
source .venv/bin/activate
```

Execute o pipeline completo:

```bash
python -m src.pipeline
```

O pipeline executa automaticamente:

```text
Extract
   ↓
Transform
   ↓
Validação
   ↓
Analysis
   ↓
Dashboard
```

Para executar os testes:

```bash
pytest -q
```

## Principais Componentes

### `src/extract.py`

Responsável pela extração dos dados brutos e carregamento dos datasets.

### `src/transform.py`

Responsável pela transformação, integração e preparação dos dados.

### `src/validacao.py`

Responsável pelas validações de qualidade dos dados.

### `src/analise.py`

Responsável pela geração das análises e datasets analíticos.

### `src/dashboard/dashboard.py`

Responsável pela geração das visualizações analíticas.

### `src/pipeline.py`

Responsável pela execução integrada de todo o fluxo de processamento.

### `tests/`

Contém os testes automatizados de qualidade e integridade dos dados.

## Controle de Versão

O projeto utiliza Git para controle de versão e organização das etapas de desenvolvimento.

Principais etapas já implementadas:

* Estrutura inicial do projeto
* Pipeline de transformação
* Modularização da extração
* Validação automatizada
* Testes de qualidade
* Integração do pipeline
* Integração da análise
* Integração do dashboard

## Próximos Passos

* Publicação no GitHub
* Integração contínua com GitHub Actions
* Migração do banco para PostgreSQL
* Dashboard interativo
* Orquestração do pipeline
* Expansão da cobertura de testes
* Documentação técnica
* Melhorias de observabilidade e logging
* Containerização com Docker
* Evolução da arquitetura para um fluxo de dados mais próximo de um ambiente de produção

