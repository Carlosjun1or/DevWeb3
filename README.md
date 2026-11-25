<div align="center">

<img src="trabalho01/projeto/static/images/logo.svg" alt="Logo Nimbo" width="110">

# ☁️ Nimbo

### Ideias digitais, do catálogo ao pedido

Aplicação web completa em **Django 5** + **PostgreSQL (Supabase)** para gestão de **serviços digitais, produtos de parceiros, carrinho de compras e equipe**

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.1.7-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3FCF8E?style=for-the-badge&logo=supabase&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST-A30000?style=for-the-badge&logo=django&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)

🛍️ **Catálogo** &nbsp;•&nbsp; 🧺 **Carrinho & Pedidos** &nbsp;•&nbsp; 👥 **Equipe (Supabase)** &nbsp;•&nbsp; 📊 **Relatórios** &nbsp;•&nbsp; 🔐 **Autenticação**

*Projeto Desenvolvido para a Disciplina de Desenvolvimento Web III • FATEC Praia Grande • DSM*

🌐 **[Acesse a Aplicação em Produção no Render](https://nimbo-web-k8xk.onrender.com)**

</div>

---

## 📑 Sumário

- [Sobre o projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#️-tecnologias)
- [Arquitetura](#️-arquitetura)
- [Integração com Supabase](#-integração-com-supabase)
- [Como executar localmente](#-como-executar-localmente)
- [Deploy no Render](#-deploy-no-render)
- [Páginas e Rotas](#-páginas-e-rotas)
- [API REST](#-api-rest)
- [Regras de negócio](#-regras-de-negócio)
- [Testes](#-testes)
- [Identidade visual](#-identidade-visual)
- [Limitações e próximos passos](#️-limitações-conhecidas)

---

## 📌 Sobre o projeto

O **Nimbo** é uma plataforma web criada para apresentar e comercializar serviços de tecnologia e design (como desenvolvimento de sites, aplicativos e identidade visual), além de integrar um ecossistema com **produtos de lojas parceiras** consumidos via API REST externa.

O sistema conta com um catálogo interativo, carrinho de compras demonstrativo persistido em sessão, histórico de pedidos por cliente, formulário de contato e um **painel administrativo completo** com relatórios analíticos de serviços e gestão de equipe integrada em tempo real com o **Supabase**.

> 💡 **Destaque da modelagem:** O banco PostgreSQL armazena no schema `django` as contas de usuários, pedidos, itens e contatos, enquanto o schema `public` gerencia os serviços e categorias. A equipe é gerenciada de forma híbrida e segura através da API do Supabase (PostgREST).

> 🧺 **Carrinho Híbrido:** O carrinho aceita simultaneamente **serviços próprios em BRL (R$)** e **produtos parceiros em USD (US$)**, agrupando os totais por moeda e gerando pedidos rastreáveis no painel do usuário.

---

## ✨ Funcionalidades

### 🛍️ Catálogo e Descoberta
- Filtros por tipo (Tudo, Serviços Nimbo ou Produtos Parceiros).
- Campo de busca instantânea com suporte a títulos, categorias e descrições.
- Exibição de disponibilidade de serviços e badges informativos.
- Visualização expansível de descrição longa (*read-more*) sem recarregar a página.

### 🧺 Carrinho e Pedidos
- Adição rápida de serviços e produtos ao carrinho com persistência em sessão (`session-based`).
- Ajuste dinâmico de quantidades (limite de 1 a 99 itens) e remoção instantânea.
- Resumo com cálculo automático de subtotais e conversão visual por moeda.
- Fechamento de pedido demonstrativo e histórico de compras em **Meus Pedidos**.

### 👥 Equipe e Institucional
- Página "Quem Somos" com listagem dinâmica dos integrantes e suas funções.
- Painel administrativo para cadastrar, editar e remover integrantes via Supabase SDK.
- Formulário de contato com validação e área restrita para consulta e exclusão de mensagens.

### 🛠️ Administração & Relatórios
- Painel analítico com contagem de serviços ativos/inativos, preço médio e destaques de menor/maior preço.
- Gestão completa (CRUD) de serviços com upload de imagens e associação de categorias.
- Controle de acesso com permissão diferenciada para administradores e clientes.

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| 🐍 **Python 3.13** | Linguagem principal do backend |
| 🌐 **Django 5.1.7** | Framework web full stack (SSR + MVT) |
| 🔌 **Django REST Framework 3.15** | Criação de endpoints REST para categorias |
| 🐘 **PostgreSQL** | Banco de dados relacional principal |
| ⚡ **Supabase** | Banco gerenciado na nuvem + SDK PostgREST (`supabase-py`) |
| 🦄 **Gunicorn 23.0** | Servidor WSGI HTTP de produção |
| 📦 **WhiteNoise 6.8** | Servidor e otimizador de arquivos estáticos (CSS/JS) |
| 🖼️ **Pillow 11.0** | Processamento e validação de uploads de imagem |
| ☁️ **Render** | Plataforma de hospedagem e CI/CD em nuvem |
| 🛍️ **FakeStoreAPI** | API externa para catálogo de produtos parceiros |
| 🎨 **CSS3 Moderno** | Layout com variáveis CSS, Flexbox, Grid e Container Queries |

---

## 🏗️ Arquitetura

```mermaid
flowchart LR
    A[🌐 Navegador] -->|HTML + CSS + JS| B[🦄 Gunicorn / Django]
    B -->|Rotas MVT| C[🎮 Apps Django]
    C -->|ORM psycopg| D[(🐘 Supabase PostgreSQL)]
    C -->|API SDK Python| E[⚡ Supabase PostgREST]
    C -->|HTTP requests| F[🛍️ FakeStoreAPI]
    B -->|WhiteNoise| G[📦 Arquivos Estáticos]
```

### 🧱 Modelo de Dados (ORM)

```mermaid
erDiagram
    USER ||--o| PERFIL : "possui (cliente/admin)"
    USER ||--o{ PEDIDO : "realiza"
    CATEGORIA ||--o{ SERVICO : "agrupa"
    SERVICO ||--o{ PEDIDO_ITEM : "origina"
    PEDIDO ||--o{ PEDIDO_ITEM : "contém"
    CONTATO {
        bigint id PK
        string nome
        string email
        string telefone
        text mensagem
        datetime criado_em
    }
    CATEGORIA {
        bigint id PK
        string nome UK
        text descricao
        boolean ativo
    }
    SERVICO {
        bigint id PK
        string nome
        text descricao
        decimal preco
        string imagem
        boolean ativo
        bigint categoria_id FK
    }
    PEDIDO {
        bigint id PK
        bigint usuario_id FK
        decimal preco
        string moeda
        datetime criado_em
    }
    PEDIDO_ITEM {
        bigint id PK
        bigint pedido_id FK
        bigint servico_id FK
        int produto_parceiro_id
        string nome
        int quantidade
        decimal preco_unitario
        string moeda
    }
```

### 📁 Estrutura de Pastas

```
DevWeb3/
├── README.md
└── trabalho01/
    ├── manage.py
    ├── requirements.txt
    ├── build.sh               # Script de automação de build para o Render
    ├── .env / .env.example
    ├── media/                 # Imagens e uploads de serviços
    ├── projeto/               # Configurações globais (settings.py, urls.py, wsgi.py)
    │   ├── templates/         # Template base compartilhado (base.html)
    │   └── static/            # CSS global, scripts de máscara e logotipo
    ├── catalogo/              # Serviços, categorias, relatórios e produtos parceiros
    ├── contas/                # Autenticação, perfis de usuário e troca de senha
    ├── pedidos/               # Carrinho em sessão, checkout e histórico de compras
    ├── web_site/              # Home, 'Quem somos', contato e painel da equipe
    ├── login/                 # Rotas legadas de login mantidas por compatibilidade
    └── ap/                    # Código arquivado da primeira versão
```

---

## ⚡ Integração com Supabase

O projeto utiliza o Supabase em duas camadas:

1. **Camada de Banco Relacional (PostgreSQL):**
   - Configurada via `DATABASE_URL` no `settings.py`.
   - Utiliza conexão pooler segura com `sslmode=require` e `search_path=django,public`.
   - As migrações do Django (`python manage.py migrate`) gerenciam tabelas de autenticação, catálogo e pedidos.

2. **Camada de API SDK (`supabase-py`):**
   - Leitura pública dos integrantes da equipe via `SUPABASE_URL` + `SUPABASE_KEY` (anon/publishable).
   - Gerenciamento restrito (inclusão, edição e exclusão) utilizando a chave `SUPABASE_SECRET_KEY` exclusivamente no backend em views protegidas com `@admin_required`.

---

## 🚀 Como Executar Localmente

### Pré-requisitos
- **Python 3.13+** instalado.
- Conta no **Supabase** (ou instância local do PostgreSQL).

### 1️⃣ Clone o repositório
```bash
git clone https://github.com/Carlosjun1or/DevWeb3.git
cd DevWeb3/trabalho01
```

### 2️⃣ Crie e ative o ambiente virtual
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instale as dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4️⃣ Configure o arquivo `.env`
Copie o modelo de exemplo e insira suas credenciais:
```bash
cp .env.example .env
```
Preencha os valores:
```ini
DATABASE_URL=postgresql://postgres.xxx:senha@host:5432/postgres?sslmode=require
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_chave_anon_publica
SUPABASE_SECRET_KEY=sua_chave_secret_role
SECRET_KEY=sua_chave_secreta_django
DEBUG=True
```

### 5️⃣ Execute as migrações e inicie o servidor
```bash
python manage.py migrate
python manage.py runserver
```

Acesse: **`http://127.0.0.1:8000/`** 🎉

---

## ☁️ Deploy no Render

A aplicação está configurada para deploy contínuo (**CI/CD**) no Render utilizando o branch **`p2`**.

- **Tipo de Serviço**: Web Service (Python 3)
- **Root Directory**: `trabalho01`
- **Build Command**: `./build.sh` (atualiza pip, instala dependências, roda `collectstatic` e aplica `migrate`)
- **Start Command**: `gunicorn projeto.wsgi:application`

### Variáveis de Ambiente no Render Dashboard:
| Variável | Valor |
|---|---|
| `DATABASE_URL` | String de conexão do Supabase com `sslmode=require` |
| `SUPABASE_URL` | URL da instância do Supabase |
| `SUPABASE_KEY` | Chave anon/publishable |
| `SUPABASE_SECRET_KEY` | Chave secreta de serviço |
| `SECRET_KEY` | Chave criptográfica única de produção |
| `DEBUG` | `False` |

---

## 🌐 Páginas e Rotas

| Página | Rota | Descrição |
|---|---|---|
| 🏠 Início | `/` | Apresentação institucional, serviços em destaque e chamada de ação |
| 🛍️ Catálogo | `/produtos/` | Vitrine integrada com serviços Nimbo e produtos parceiros |
| 🧺 Carrinho | `/pedidos/carrinho/` | Visualização dos itens da sacola, ajuste de quantidade e totalizadores |
| 📦 Meus Pedidos | `/pedidos/meus-pedidos/` | Histórico dos pedidos realizados pelo cliente logado |
| 👥 Quem Somos | `/quem-somos/` | Apresentação da equipe de especialistas carregada do Supabase |
| ✉️ Contato | `/contato/` | Formulário para envio de dúvidas e orçamentos |
| 🔐 Entrar / Cadastrar | `/contas/` e `/contas/cadastro/` | Autenticação, criação de perfil e recuperação de senha |
| 📊 Dashboard | `/contas/dashboard/` | Central de navegação e atalhos para áreas do sistema |
| ⚙️ Gestão de Serviços | `/catalogo/servicos/` | Painel administrativo com filtros e cadastro de serviços |
| 📈 Relatórios | `/catalogo/relatorios/` | Gráficos e indicadores analíticos de precificação e disponibilidade |
| 🧑‍💼 Painel da Equipe | `/painel/equipe/` | CRUD restrito de integrantes conectado à API do Supabase |
| 📬 Contatos Admin | `/contatos/` | Listagem e moderação de mensagens recebidas |

---

## 🔌 API REST

Endpoints REST disponíveis via Django REST Framework:

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/catalogo/api/categorias/` | Listar todas as categorias cadastradas |
| `POST` | `/catalogo/api/categorias/` | Cadastrar uma nova categoria |
| `GET` | `/catalogo/api/categorias/{id}/` | Detalhes de uma categoria específica |
| `PUT` | `/catalogo/api/categorias/{id}/` | Atualizar dados da categoria |
| `DELETE` | `/catalogo/api/categorias/{id}/` | Remover categoria |

---

## 🧠 Regras de Negócio

### 🛍️ Catálogo & Serviços
- O preço de serviços é formatado em moeda brasileira (BRL) e aceita pontuação com vírgula ou ponto (`R$ 0,00`).
- Não é possível excluir uma categoria que possua serviços vinculados (`on_delete=models.PROTECT`).
- Imagens enviadas são armazenadas e servidas de forma estática com cache em disco.

### 🧺 Carrinho & Pedidos
- O carrinho aceita quantidades entre 1 e 99 unidades por item.
- Serviços e produtos parceiros possuem moedas distintas (BRL e USD), com totalizadores separados no fechamento.
- Para concluir a compra, o usuário deve estar autenticado. Ao finalizar, os itens da sessão são convertidos em registros persistentes de `Pedido` e `PedidoItem`.

### 👥 Equipe & Supabase
- Somente usuários com permissão de administrador (`@admin_required`) podem incluir, editar ou remover integrantes do Supabase.
- Caso a API externa de integrantes fique temporariamente indisponível, a aplicação exibe um alerta amigável sem quebrar o layout.

---

## 🧪 Testes

Para executar os testes automatizados do Django:

```bash
cd trabalho01
python manage.py test
```

Durante a execução da suíte de testes, o Django inicializa automaticamente um banco **SQLite em memória**, mantendo os testes rápidos, isolados e sem afetar os dados reais do PostgreSQL/Supabase.

---

## 🎨 Identidade Visual

O design do Nimbo transmite leveza, modernidade e tecnologia:

| Cor | Hex | Uso |
|---|---|---|
| 🟣 Violeta Nimbo | `#5B3DF5` | Botões principais, links e destaque de marca |
| 🔮 Violeta Escuro | `#3F27C7` | Hover e elementos em foco |
| 🌌 Tinta Escura | `#1B1840` | Headers escuros, textos principais e hero |
| 🌸 Lilás Suave | `#E9E4FF` | Badges, fundos de destaque e cartões de apoio |
| ☀️ Amarelo Sol | `#FFC94A` | Acento, kickers em contraste e sol no logo |
| 📄 Fundo da Página | `#F7F5FF` | Fundo geral da aplicação |

Fontes utilizadas: **Space Grotesk** (títulos marcantes) e **Inter** (textos e dados com alta legibilidade).

---

## ⚠️ Limitações Conhecidas

- O ambiente gratuito do Render reinicia o sistema de arquivos efêmero a cada novo deploy, de modo que novos uploads locais de imagem na pasta `media/` requerem armazenamento persistente em nuvem (ex.: Supabase Storage ou AWS S3) para retenção de longo prazo.
- O checkout de pedidos é demonstrativo e focado no fluxo operacional, sem gateway de pagamento real acoplado.

---

<div align="center">

Desenvolvido por **Carlos Junior** com Django & Supabase 🚀  
⭐ Se curtiu o projeto, deixe uma estrela no repositório!

</div>
