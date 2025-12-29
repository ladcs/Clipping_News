# 📌 Clipping News

Clipping News é um projeto voltado para a automação do processo de clipping de notícias, com foco no mercado financeiro.

O clipping é uma atividade tradicionalmente utilizada para coletar, organizar e resumir conteúdos relevantes, entregando essas informações de forma estruturada para tomada de decisão. Embora hoje seja menos comum como serviço manual, ele se torna extremamente poderoso quando aliado à automação, dados estruturados e inteligência artificial.

Este projeto nasce justamente dessa proposta: automatizar o clipping financeiro, desde a coleta até a análise do impacto das notícias.

## 🎯 Objetivo do Projeto

Coletar notícias financeiras de forma legal e estruturada

Centralizar conteúdos em um banco de dados relacional

Relacionar notícias com ativos financeiros e suas variações

Preparar a base para análises automatizadas e uso de IA generativa

## 📰 Coleta de Dados

Inicialmente, foi considerada a utilização de raspagem de dados (web scraping). No entanto, nem todos os portais permitem esse tipo de coleta, o que pode gerar problemas legais e técnicos.

Como alternativa, o projeto adotou o uso de RSS (Really Simple Syndication), uma tecnologia amplamente utilizada por portais de notícias para distribuição oficial de conteúdo.

As fontes de dados foram obtidas a partir de:

Feeds RSS oficiais dos próprios portais

Agregadores de RSS, como Feedspot

Portais de economia e finanças que disponibilizam feeds públicos

Essa abordagem garante:

Maior confiabilidade dos dados

Menor risco legal

Atualizações contínuas e padronizadas

🗄️ Banco de Dados

O projeto utiliza PostgreSQL, executando em ambiente Docker, para armazenar e organizar todas as informações coletadas.

A modelagem foi pensada para:

Escalar o projeto no futuro

Relacionar notícias com ativos financeiros

Permitir análises históricas

Suportar automações e inteligência artificial

## 📐 Modelagem do Banco de Dados

erDiagram
    NEWS_SOURCES {
        int id PK
        text label
        text source_link
        boolean is_scratch
        boolean need_summary
        timestamp created_at
        timestamp updated_at
        timestamp deleted_at
    }

    NEWS {
        int id PK
        int source_id FK
        text title
        text link
        text summary
        text content
        text about
        timestamp datetime
        timestamp created_at
        timestamp updated_at
        timestamp deleted_at
    }

    ACTIVES {
        int id PK
        text name
        boolean is_cripto
        timestamp created_at
        timestamp updated_at
        timestamp deleted_at
    }

    CHANGES {
        int id PK
        int active_id FK
        float active_value
        float active_value_prev
        timestamp created_at
        timestamp updated_at
        timestamp deleted_at
    }

    CHANGE_REASONS {
        int id PK
        int active_id FK
        int change_id FK
        int news_id FK
        text label
        float porcent
        timestamp created_at
        timestamp updated_at
        timestamp deleted_at
    }

## 🧠 Visão Geral das Tabelas

news_sources
Representa a origem das notícias (RSS, scraping, APIs externas).

news
Armazena as notícias coletadas, incluindo resumo, conteúdo e data original de publicação.

actives
Cadastro de ativos financeiros (ações, criptomoedas, etc).

changes
Registro de variações de valor dos ativos ao longo do tempo.

change_reasons
Relaciona notícias com variações de ativos, permitindo análises de causa e efeito.

Todas as tabelas utilizam soft delete (deleted_at) e possuem controle automático de atualização (updated_at via trigger).

## 🔮 Evolução do Projeto

Apesar de o projeto conter mais tabelas do que o necessário neste primeiro momento, a modelagem foi pensada para crescimento futuro, permitindo:

Integração com ferramentas de automação (ex: n8n)

Uso de IA para:

Resumo automático de notícias

Classificação de impacto

Identificação de ativos citados

Criação de dashboards e análises históricas

Expansão para outros domínios além de finanças

## 🚀 Tecnologias Utilizadas

PostgreSQL

Docker / Docker Compose

Python

RSS / Feeds

n8n (planejado)

IA Generativa (planejado)