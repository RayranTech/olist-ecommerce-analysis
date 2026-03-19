# 📦 Análise de E-commerce — Olist

> Análise completa de dados de um e-commerce brasileiro com SQL avançado, Python e dashboard interativo no Power BI.

![Dashboard](reports/dashboard.png)

---

## 📌 Contexto

A Olist é uma plataforma brasileira que conecta pequenos lojistas a grandes marketplaces. Este projeto analisa **99.441 pedidos** realizados entre setembro de 2016 e setembro de 2018, respondendo a perguntas estratégicas de negócio sobre receita, satisfação de clientes e logística.

---

## ❓ Problema de Negócio

> *Quais categorias, regiões e períodos geram mais receita — e onde estão os maiores gargalos de entrega e satisfação do cliente?*

A partir dessa pergunta central, três hipóteses foram investigadas:

1. O tempo de entrega impacta diretamente a avaliação do cliente?
2. Existe concentração geográfica de receita?
3. Qual é a taxa de retenção de clientes da plataforma?

---

## 🗂️ Estrutura do Projeto

```
olist-ecommerce-analysis/
│
├── data/                          # Dados brutos (não versionados)
│   └── vendas_mensais.csv         # Agregação mensal gerada pelo pipeline
│
├── notebooks/
│   ├── importar_dados.ipynb       # Carga dos CSVs no PostgreSQL
│   └── exploracao_inicial.ipynb   # Análise exploratória e geração de gráficos
│
├── sql/
│   ├── criar_tabelas.ipynb        # DDL das tabelas no PostgreSQL
│   └── analises.sql               # Queries de análise de negócio
│
├── dashboard/                     # Arquivo Power BI (.pbix)
│
├── reports/                       # Gráficos e imagens exportados
│
└── README.md
```

---

## 🛠️ Tecnologias Utilizadas

| Ferramenta | Uso |
|---|---|
| **Python 3** | Limpeza, transformação e análise exploratória |
| **Pandas** | Manipulação de DataFrames |
| **Matplotlib / Seaborn** | Visualizações exploratórias |
| **PostgreSQL** | Banco de dados relacional para armazenamento e consultas |
| **SQLAlchemy** | Conexão Python ↔ PostgreSQL |
| **SQL (CTEs + Window Functions)** | Análises avançadas de negócio |
| **Power BI** | Dashboard interativo com DAX |
| **Git / GitHub** | Versionamento de código |

---

## 🔄 Pipeline de Dados

```
Kaggle (CSV brutos)
       │
       ▼
importar_dados.ipynb
  └── Carrega CSVs via Pandas
  └── Insere tabelas no PostgreSQL via SQLAlchemy
       │
       ▼
PostgreSQL (banco: olist)
  └── orders, order_items, customers
  └── products, reviews, category_translation
  └── vendas_mensais (agregada pelo Python)
       │
       ▼
exploracao_inicial.ipynb
  └── Limpeza e conversão de tipos
  └── Cálculo de métricas de negócio
  └── Geração de gráficos exploratórios
  └── Exportação de dados tratados
       │
       ▼
sql/analises.sql
  └── Queries com CTEs e Window Functions
  └── Análises por estado, categoria e tempo de entrega
       │
       ▼
Power BI (conectado ao PostgreSQL)
  └── Medidas DAX
  └── Dashboard interativo
```

---

## 📊 Principais Análises

### 1. Evolução de Receita Mensal
A receita cresceu de forma consistente entre janeiro e novembro de 2017, atingindo o pico de **R$ 1 milhão** em novembro de 2017 — possivelmente impulsionado pela Black Friday. A queda em setembro de 2018 é explicada pelo corte do dataset no meio do mês.

### 2. Top 10 Categorias por Receita
| Categoria | Receita Total | % da Receita |
|---|---|---|
| health_beauty | R$ 1.233.131 | 9,45% |
| watches_gifts | R$ 1.166.176 | 8,94% |
| bed_bath_table | R$ 1.023.434 | 7,85% |
| sports_leisure | R$ 954.852 | 7,32% |
| computers_accessories | R$ 888.724 | 6,81% |

### 3. Receita por Estado
São Paulo concentra **R$ 5 milhões** em receita — quase 40% do total. Porém, estados do Nordeste como Paraíba (PB) e Alagoas (AL) apresentam os maiores tickets médios, indicando oportunidade de crescimento nessas regiões.

### 4. Tempo de Entrega vs. Avaliação ⭐
| Nota | Tempo médio de entrega |
|---|---|
| ⭐ 1 | 20,9 dias |
| ⭐ 2 | 16,2 dias |
| ⭐ 3 | 13,8 dias |
| ⭐ 4 | 11,8 dias |
| ⭐ 5 | 10,2 dias |

Clientes que recebem em até 10 dias dão nota 5. Clientes que esperam mais de 20 dias dão nota 1. **A correlação é direta e linear.**

### 5. Taxa de Recompra
| Pedidos por cliente | % de clientes |
|---|---|
| 1 pedido | 97,00% |
| 2 pedidos | 2,76% |
| 3+ pedidos | 0,24% |

**97% dos clientes compraram apenas uma vez.** A plataforma depende quase inteiramente de aquisição de novos clientes para crescer.

---

## 💡 Insights e Recomendações

### Insight 1 — Entrega é o principal driver de satisfação
Reduzir o tempo médio de entrega de 20 para 12 dias nos pedidos com nota baixa poderia elevar a avaliação média de 1 para 3-4 estrelas. Isso impacta diretamente reputação e recompra.

**Recomendação:** Priorizar parceiros logísticos com melhor SLA nas regiões com maior tempo de entrega, especialmente Norte e Nordeste.

### Insight 2 — Taxa de retenção crítica
Com 97% dos clientes fazendo apenas uma compra, o custo de aquisição de clientes (CAC) é muito alto. Programas de fidelidade ou cupons para segunda compra poderiam ter alto impacto.

**Recomendação:** Implementar campanha de reativação para os 90.557 clientes que compraram apenas uma vez, com foco nas categorias de maior ticket médio (watches_gifts, R$ 199).

---

## 📁 Como Reproduzir

### Pré-requisitos
- Python 3.8+
- PostgreSQL 13+
- Power BI Desktop

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/RayranTech/olist-ecommerce-analysis.git
cd olist-ecommerce-analysis

# 2. Instale as dependências
pip install pandas matplotlib seaborn sqlalchemy psycopg2-binary jupyter

# 3. Baixe o dataset
# Acesse: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
# Extraia os CSVs na pasta /data

# 4. Crie o banco de dados
# No PostgreSQL: CREATE DATABASE olist;
# Execute: sql/criar_tabelas.sql

# 5. Execute os notebooks em ordem
# notebooks/importar_dados.ipynb
# notebooks/exploracao_inicial.ipynb

# 6. Execute as queries SQL
# sql/analises.sql

# 7. Abra o dashboard
# dashboard/ → conecte ao PostgreSQL local
```

---

## 📬 Contato

Feito por **Rayran** — [GitHub](https://github.com/RayranTech) · [LinkedIn](#)

---

*Dataset: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — disponível no Kaggle sob licença CC BY-NC-SA 4.0*