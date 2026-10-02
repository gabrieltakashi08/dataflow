# DataFlow — Enterprise Sales Data Platform

Pipeline de dados desenvolvido em Python para processamento, transformação e análise de dados de vendas.

## Objetivo

O DataFlow foi desenvolvido para demonstrar um fluxo completo de dados, desde os dados brutos até a geração de análises, indicadores e visualizações de negócio.

## Pipeline

```text
Dados Brutos
     ↓
Transformação
     ↓
Dados Processados
     ↓
Análise
     ↓
Datasets Analíticos
     ↓
Visualizações
     ↓
KPIs
```

## Estrutura do projeto

```text
dataflow/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── analytics/
│
├── src/
│   ├── transform.py
│   ├── analise.py
│   ├── visualizacoes/
│   │   └── graficos.py
│   └── dashboard/
│       └── dashboard.py
│
└── README.md
```

## Tecnologias

* Python
* Pandas
* Matplotlib
* SQLite
* SQL
* Git

## Processamento

O pipeline realiza:

* Conversão e tratamento de datas
* Tratamento de valores numéricos
* Criação de métricas temporais
* Integração entre vendas e clientes
* Validação de valores nulos
* Geração de dados processados
* Geração de datasets analíticos

## Análises

### Clientes

* Faturamento por cliente
* Quantidade de compras
* Ticket médio
* Participação no faturamento
* Top clientes
* Concentração de faturamento

### Vendas

* Faturamento total
* Quantidade de vendas
* Maior venda
* Menor venda
* Mediana
* Desvio padrão
* Ticket médio

### Análise temporal

* Faturamento mensal
* Crescimento mensal
* Crescimento entre períodos
* Faturamento acumulado
* Quantidade de vendas por mês
* Ticket médio mensal

### Geografia

* Faturamento por cidade
* Quantidade de vendas por cidade
* Ticket médio por cidade
* Participação das cidades no faturamento

## Indicadores atuais

O dataset analisado possui:

* 50 vendas
* 20 clientes
* 20 cidades
* R$ 8.803,30 de faturamento total
* R$ 176,07 de ticket médio

## Visualizações

O projeto gera gráficos de:

* Evolução do faturamento mensal
* Top 10 clientes
* Top 10 cidades
* Ticket médio mensal
* Faturamento mensal
* Faturamento por cidade
* Ticket médio por cidade

## Execução

Ative o ambiente virtual:

```bash
source .venv/bin/activate
```

Execute a transformação:

```bash
python src/transform.py
```

Execute as análises:

```bash
python src/analise.py
```

Execute o dashboard:

```bash
python src/dashboard/dashboard.py
```

Os resultados são armazenados em:

```text
data/processed/
data/analytics/
```

## Próximos passos

* Implementar testes automatizados
* Melhorar validações de qualidade dos dados
* Automatizar o pipeline
* Adicionar PostgreSQL
* Criar dashboard interativo
* Implementar orquestração
* Adicionar documentação técnica

