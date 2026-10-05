# DataFlow — Enterprise Sales Data Platform

Plataforma de dados de vendas desenvolvida em Python, PostgreSQL, SQL analítico e Streamlit, com pipeline de **ETL, validação, análise, visualização e interpretação assistida por IA**.

O DataFlow foi desenvolvido como projeto de portfólio com foco em Engenharia de Dados, Analytics Engineering, qualidade de dados e integração entre dados estruturados e inteligência artificial.

---

## Visão geral

O DataFlow transforma dados comerciais brutos em informações analíticas e indicadores de negócio.

```text
CSV / Dados Brutos
        │
        ▼
     Extract
        │
        ▼
    Transform
        │
        ▼
    Validação
        │
        ▼
    PostgreSQL
        │
        ├───────────────┐
        ▼               ▼
 Analytics Engine    Data Access
        │               │
        └───────┬───────┘
                ▼
        Dashboard Streamlit
                │
                ▼
          AI Analyst
```

O projeto combina:

* ETL em Python;
* PostgreSQL;
* SQL analítico;
* funções de janela;
* CTEs;
* análise temporal;
* análise de clientes, produtos e estoque;
* validação de qualidade de dados;
* dashboard interativo;
* AI Analyst baseado nos resultados calculados pelo Analytics Engine;
* testes automatizados;
* GitHub Actions.

---

## Principais funcionalidades

### Pipeline de dados

* Extração de dados CSV;
* Transformação e padronização;
* Validação de qualidade;
* Carga no PostgreSQL;
* geração de datasets analíticos;
* execução reproduzível do pipeline.

### Analytics Engine

A camada analítica centraliza consultas SQL responsáveis por indicadores e análises como:

* faturamento mensal;
* crescimento mensal;
* ranking de clientes;
* Pareto de clientes;
* ranking de produtos;
* análise de estoque;
* análise temporal;
* análise por categoria;
* análise por cliente;
* contribuição das variações mensais.

As consultas utilizam recursos do PostgreSQL como:

* `JOIN`;
* `GROUP BY`;
* `CTE`;
* `RANK()`;
* `LAG()`;
* funções de janela;
* agregações;
* `DATE_TRUNC`;
* análise temporal.

### Dashboard

O projeto possui um dashboard interativo desenvolvido com Streamlit.

O dashboard é dividido em:

1. **Visão Geral**
2. **Clientes**
3. **Produtos**
4. **Vendas**
5. **Análises**
6. **AI Analyst**

A interface permite explorar os principais indicadores e análises da plataforma sem executar consultas SQL manualmente.

### AI Analyst

O DataFlow possui uma camada de inteligência artificial capaz de interpretar os resultados produzidos pelo Analytics Engine.

O usuário pode fazer perguntas em linguagem natural, como:

> Qual foi o mês de maior faturamento?

ou:

> Por que novembro teve faturamento maior que outubro?

A IA recebe um contexto analítico estruturado produzido pelo próprio DataFlow.

A arquitetura foi projetada para que a IA:

* utilize somente dados fornecidos pelo Analytics Engine;
* não execute SQL diretamente;
* não invente métricas;
* diferencie fatos observados de interpretações;
* apresente valores absolutos e percentuais quando disponíveis;
* declare quando uma informação não está disponível.

Isso reduz o risco de respostas desconectadas dos dados reais da plataforma.

---

## Arquitetura

```text
data/raw/
    │
    ▼
src/extract.py
    │
    ▼
src/transform.py
    │
    ▼
src/validacao.py
    │
    ▼
src/load_postgres.py
    │
    ▼
PostgreSQL
    │
    ▼
src/analytics/
    ├── queries.py
    └── service.py
    │
    ├───────────────┐
    ▼               ▼
src/data/       src/ai/
postgres.py     context.py
                analyst.py
                prompts.py
    │               │
    └───────┬───────┘
            ▼
src/dashboard/app.py
            │
            ▼
       Streamlit
```

---

## Estrutura do projeto

```text
dataflow/
├── data/
│   ├── raw/
│   ├── processed/
│   └── analytics/
│
├── database/
│   └── vendas.db
│
├── sql/
│   └── schema.sql
│
├── src/
│   ├── __init__.py
│   ├── analise.py
│   ├── extract.py
│   ├── transform.py
│   ├── validacao.py
│   ├── load_postgres.py
│   ├── pipeline.py
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── analyst.py
│   │   ├── context.py
│   │   └── prompts.py
│   │
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── queries.py
│   │   └── service.py
│   │
│   ├── dashboard/
│   │   ├── app.py
│   │   └── dashboard.py
│   │
│   ├── data/
│   │   └── postgres.py
│   │
│   └── visualizacoes/
│       ├── __init__.py
│       └── graficos.py
│
├── tests/
│   ├── __init__.py
│   └── test_data_quality.py
│
├── .github/
│   └── workflows/
│       └── dataflow.yml
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Pipeline de dados

### 1. Extract

Os dados brutos são carregados a partir de arquivos CSV utilizando Pandas.

Datasets:

* clientes;
* fornecedores;
* produtos;
* vendas;
* itens de venda;
* estoque.

### 2. Transform

O processo de transformação realiza operações como:

* tratamento de datas;
* criação de períodos temporais;
* tratamento de valores numéricos;
* integração entre entidades;
* preparação dos datasets analíticos.

### 3. Validação

Antes das etapas analíticas, são realizadas verificações de qualidade, incluindo:

* existência de colunas obrigatórias;
* valores nulos;
* registros duplicados;
* valores de venda inválidos;
* datas inválidas;
* identificadores de vendas;
* identificadores de clientes;
* consistência dos datasets esperados.

### 4. Load

Os dados são carregados para PostgreSQL utilizando `psycopg2`.

O banco possui as entidades:

* `clientes`;
* `fornecedores`;
* `produtos`;
* `vendas`;
* `itens_venda`;
* `estoque`.

O PostgreSQL é a **fonte oficial utilizada pelo Analytics Engine**.

---

## Analytics Engine

A camada `src/analytics/` separa a lógica de análise da interface do dashboard.

### Consultas implementadas

#### Faturamento

* faturamento mensal;
* quantidade de vendas;
* ticket médio;
* crescimento percentual;
* variação absoluta.

#### Clientes

* ranking de clientes;
* quantidade de compras;
* ticket médio;
* Pareto de faturamento;
* análise mensal por cliente.

#### Produtos

* ranking de produtos;
* quantidade vendida;
* análise de mix;
* análise mensal por produto.

#### Categorias

* quantidade vendida;
* análise mensal;
* composição do mix por categoria.

#### Estoque

* estoque atual;
* estoque mínimo;
* identificação de itens críticos.

---

## Qualidade e semântica dos dados

Uma preocupação importante do projeto foi não assumir que diferentes fontes representam necessariamente a mesma métrica.

O **faturamento oficial** do DataFlow é calculado a partir de:

```sql
vendas.valor_total
```

As informações de `itens_venda` são utilizadas principalmente para análise de:

* quantidade vendida;
* mix de produtos;
* composição por categoria;
* distribuição de itens.

Os valores derivados de `quantidade × preco_uni` em `itens_venda` não são utilizados automaticamente como substitutos do faturamento oficial.

Essa separação evita atribuir ao nível de produto ou categoria uma contribuição de receita que não possa ser reconciliada com os valores oficiais das vendas.

Essa abordagem também faz parte da camada de **Data Quality e Data Semantics** do projeto.

---

## Indicadores do dataset

O dataset atual contém:

| Indicador          |       Valor |
| ------------------ | ----------: |
| Vendas             |          50 |
| Clientes           |          20 |
| Faturamento total  | R$ 8.803,30 |
| Ticket médio       |   R$ 176,07 |
| Maior venda        |   R$ 512,70 |
| Menor venda        |    R$ 42,90 |
| Mediana das vendas |   R$ 145,95 |
| Desvio padrão      |   R$ 111,68 |

Faturamento mensal:

| Mês           | Faturamento |
| ------------- | ----------: |
| Julho/2025    | R$ 1.371,40 |
| Agosto/2025   | R$ 1.787,80 |
| Setembro/2025 | R$ 1.665,60 |
| Outubro/2025  | R$ 1.921,10 |
| Novembro/2025 | R$ 2.057,40 |

---

## Testes

O projeto utiliza Pytest para validação automatizada.

Entre as verificações realizadas estão:

* existência dos datasets;
* integridade dos dados;
* ausência de valores nulos;
* ausência de duplicidades;
* quantidade esperada de vendas;
* valores positivos;
* existência dos KPIs;
* existência dos datasets analíticos;
* execução da validação completa.

Os testes também são executados pelo workflow de CI configurado no GitHub Actions.

---

## Integração contínua

O projeto possui GitHub Actions para automatizar etapas do processo de validação.

O workflow realiza:

1. checkout do código;
2. configuração do Python;
3. instalação das dependências;
4. configuração do PostgreSQL;
5. criação do schema;
6. execução do pipeline;
7. execução dos testes.

---

## Tecnologias

### Linguagem

* Python 3.11

### Dados

* PostgreSQL
* SQL
* Pandas
* psycopg2
* SQLite

### Analytics

* CTEs
* Window Functions
* `RANK()`
* `LAG()`
* `GROUP BY`
* `JOIN`
* agregações
* análise temporal

### Visualização

* Streamlit
* Matplotlib

### Qualidade

* Pytest
* validações de dados
* GitHub Actions

### Inteligência Artificial

* OpenAI API
* arquitetura de contexto analítico
* análise em linguagem natural

### Versionamento

* Git
* GitHub

---

## Como executar

### 1. Clonar o projeto

```bash
git clone git@github.com:gabrieltakashi08/dataflow.git
cd dataflow
```

### 2. Criar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar PostgreSQL

Defina a senha do usuário PostgreSQL utilizado pelo projeto:

```bash
export DATAFLOW_DB_PASSWORD="sua_senha"
```

### 5. Configurar a IA

Para utilizar o AI Analyst:

```bash
export OPENAI_API_KEY="sua_chave"
```

As credenciais **não devem ser armazenadas no código-fonte ou commitadas no Git**.

### 6. Executar o pipeline

```bash
python -m src.pipeline
```

### 7. Executar os testes

```bash
python -m pytest -v
```

### 8. Executar o dashboard

```bash
export PYTHONPATH="$PWD"
streamlit run src/dashboard/app.py
```

O Streamlit disponibilizará a aplicação localmente.

---

## Segurança

Credenciais e informações sensíveis são tratadas por variáveis de ambiente.

O projeto não deve armazenar:

* API keys;
* senhas;
* tokens;
* arquivos `.env`;
* credenciais de banco.

Esses arquivos e variáveis são protegidos pelo `.gitignore` e pela configuração de ambiente.

---

## Próximas evoluções

Possíveis evoluções técnicas do projeto:

* maior cobertura de testes;
* observabilidade e logging;
* métricas de performance;
* otimização adicional das consultas SQL;
* containerização com Docker;
* orquestração do pipeline;
* camada de cache;
* autenticação do dashboard;
* monitoramento de qualidade dos dados;
* evolução para uma arquitetura próxima de um ambiente produtivo.

---

## Objetivo do projeto

O DataFlow foi desenvolvido como um projeto prático de Engenharia de Dados para demonstrar a integração entre:

```text
Data Engineering
       +
SQL Analytics
       +
Data Quality
       +
Visualization
       +
Artificial Intelligence
```

O objetivo não é apenas gerar gráficos, mas construir uma pequena plataforma de dados capaz de **extrair, validar, armazenar, consultar, analisar e interpretar informações de negócio de forma estruturada e reproduzível**.
