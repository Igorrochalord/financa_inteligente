# 🚀 Finança Pro

O **Finança Pro** é um ecossistema de gestão financeira pessoal e monitoramento de ativos da B3 em tempo real. Desenvolvido com foco em **performance, escalabilidade e observabilidade**, o projeto integra análise de dados financeiros, scraping de notícias e persistência em banco de dados NoSQL.

## 🛠️ Stack Tecnológica

* **Frontend/Interface:** [Streamlit](https://streamlit.io/) (UI reativa e moderna em Python).
* **Backend:** Python 3.12+ com integração Assíncrona.
* **Banco de Dados:** [MongoDB](https://www.mongodb.com/) (Persistência de transações, portfólio e cache de mercado).
* **Infraestrutura:** Docker & Docker-Compose (Containerização completa do ambiente).
* **APIs Financeiras:** Yahoo Finance (`yfinance`) para cotações e gráficos Candlestick.

---

## ✨ Principais Funcionalidades

### 📈 Terminal de Mercado

* **Trading Engine:** Sistema de ordens de compra e venda com atualização automática de preço médio e abatimento de saldo no MongoDB.
* **Gráficos Candlestick:** Visualização técnica de ativos com diferentes períodos (1m, 6m, 1y).
* **Market Movers:** Painel de Maiores Altas e Baixas do IBOVESPA com **Cache Persistente** no MongoDB para otimização de requisições à API.

### 🏦 Gestão Patrimonial

* **KPIs Inteligentes:** Monitoramento de Saldo Líquido, Gastos Mensais e Patrimônio Investido.
* **Recomendações Dinâmicas:** Motor de sugestões que analisa o saldo disponível e recomenda aportes em ativos específicos (ex: MXRF11.SA).
* **Relatórios PDF:** Geração de snapshots financeiros exportáveis.

### 📰 Inteligência de Dados

* **News Scraper:** Captura de manchetes financeiras do **Poder360** e **CNN Money** via BeautifulSoup.
* **Interleave Algorithm:** Algoritmo que intercala fontes de notícias para um feed equilibrado e visualmente organizado com logos locais.

---

## 🏗️ Arquitetura e DevOps

O projeto foi desenhado para rodar em ambientes isolados, garantindo que o banco de dados e a aplicação se comuniquem via rede interna do Docker.

### Estrutura de Pastas

```text
financa_inteligente/
├── assets/          # Logos SVG e Estilos CSS
├── src/
│   ├── api_client/  # Motor de integração com Yahoo Finance e Cache
│   ├── database/    # Singleton de conexão com MongoDB
│   ├── views/       # Camada de apresentação (Dashboard/Login)
│   └── news/        # Scraper e lógica de cache de notícias
├── app.py           # Entry point da aplicação
└── docker-compose.yml

```

---

## 🚀 Como Executar

### Pré-requisitos

* Docker e Docker-Compose instalados.
* Arquivos de logo (`poder_5.svg` e `log-cnn-money.svg`) na pasta `/assets`.

### Passo a Passo

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/financa-pro.git

```


2. Suba os containers:
```bash
docker-compose up --build

```


3. Acesse em seu navegador:
```text
http://localhost:8501

```



---

## 📅 Roadmap de Evolução

* [ ] **Histórico de Patrimônio:** Implementação de snapshots diários para gráficos de evolução temporal.
* [ ] **Alertas via Telegram:** Bot para notificar variações bruscas no mercado e bater metas de saldo.
* [ ] **Observabilidade:** Endpoint de métricas para integração com Prometheus/Grafana.

---

**Desenvolvido por [Igor Rocha**](https://www.google.com/search?q=https://www.linkedin.com/in/igor-rocha-0bb14521a/) *Backend & DevOps Engineer | Especialista em Arquiteturas de Alta Disponibilidade*

---
