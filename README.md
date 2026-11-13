<div align="center">

<img src="trabalho01/projeto/static/images/logo.svg" alt="Nimbo" width="92" />

# Nimbo · ideias digitais, do catálogo ao pedido

Uma vitrine digital para descobrir serviços, conhecer a equipe e transformar escolhas em pedidos — com uma área administrativa para manter tudo em movimento.

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1.7-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Supabase](https://img.shields.io/badge/Supabase-integrado-3FCF8E?logo=supabase&logoColor=white)](https://supabase.com/)

**[Começar agora](#-comece-em-poucos-minutos)** ·
**[Ver funcionalidades](#-o-que-voc%C3%AA-encontra)** ·
**[Configurar o Supabase](#-configure-o-supabase)** ·
**[Executar os testes](#-testes)** ·
**[Contribuir](#-contribua)**

</div>

---

<details open>
<summary><strong>🧭 Navegação rápida</strong></summary>

- [O projeto](#-o-projeto)
- [O que você encontra](#-o-que-voc%C3%AA-encontra)
- [Comece em poucos minutos](#-comece-em-poucos-minutos)
- [Configure o Supabase](#-configure-o-supabase)
- [Mapa do projeto](#-mapa-do-projeto)
- [Rotas úteis](#-rotas-%C3%BAteis)
- [Testes](#-testes)
- [Segurança e configuração](#-seguran%C3%A7a-e-configura%C3%A7%C3%A3o)
- [Contribua](#-contribua)

</details>

## ✨ O projeto

O **Nimbo** é uma aplicação web feita com Django para apresentar serviços, receber mensagens, organizar pedidos e administrar o conteúdo do site. O catálogo reúne serviços próprios e produtos de lojas parceiras; contas de clientes e pedidos ficam associados ao banco PostgreSQL configurado para o projeto.

> **Em uma frase:** uma experiência integrada para quem visita a loja e ferramentas práticas para quem administra.

## 🚀 O que você encontra

<table>
  <tr>
    <td width="50%">
      <h3>🛍️ Catálogo e descoberta</h3>
      <p>Consulte serviços, veja disponibilidade, pesquise e explore produtos de parceiros.</p>
    </td>
    <td width="50%">
      <h3>🧺 Carrinho e pedidos</h3>
      <p>Adicione itens, atualize o carrinho e acompanhe pedidos na sua conta.</p>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>👥 Equipe e contato</h3>
      <p>Conheça a equipe e envie mensagens pelo formulário de contato.</p>
    </td>
    <td width="50%">
      <h3>🛠️ Administração</h3>
      <p>Gerencie serviços, equipe e contatos; consulte relatórios e áreas protegidas.</p>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>🔐 Contas de usuário</h3>
      <p>Cadastre-se, entre, edite seu perfil e gerencie sua senha.</p>
    </td>
    <td width="50%">
      <h3>☁️ Supabase</h3>
      <p>Integração para consultar dados públicos e administrar integrantes com uma chave secreta apenas no servidor.</p>
    </td>
  </tr>
</table>

<details>
<summary><strong>🧑‍💻 Quer ver o fluxo da aplicação?</strong></summary>

1. A pessoa explora o catálogo e escolhe serviços ou produtos parceiros.
2. Os itens selecionados podem ser organizados no carrinho.
3. Para acompanhar pedidos e acessar recursos da conta, é necessário entrar.
4. Pessoas autorizadas podem administrar serviços, contatos e equipe.

</details>

## ⚡ Comece em poucos minutos

### 1. Pré-requisitos

- Python instalado (o projeto foi verificado com Python 3.13).
- Acesso a um banco PostgreSQL usado pelo Supabase.
- Credenciais do projeto Supabase para os recursos de equipe.

### 2. Prepare o ambiente

Abra um terminal na raiz do repositório:

```powershell
cd .\trabalho01
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

> No Windows, caso o PowerShell bloqueie a ativação do ambiente, execute `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` e tente novamente. No CMD, ative com `venv\Scripts\activate`.

<details>
<summary><strong>🍎 Linux ou macOS</strong></summary>

Execute os comandos abaixo na pasta do repositório:

```bash
cd trabalho01
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

</details>

### 3. Preencha o `.env`

Abra `trabalho01/.env` e substitua os valores de exemplo pelas credenciais do seu ambiente. Consulte [Configurar o Supabase](#-configure-o-supabase) para entender cada variável.

### 4. Prepare o banco e inicie

```powershell
python manage.py migrate
python manage.py runserver
```

Abra **http://127.0.0.1:8000/** no navegador.

> O projeto exige `DATABASE_URL` apontando para PostgreSQL fora dos testes. Ele **não** troca automaticamente para SQLite em execução normal.

## ☁️ Configure o Supabase

O arquivo [`trabalho01/.env.example`](trabalho01/.env.example) é um modelo seguro: contém apenas placeholders, nunca credenciais reais.

| Variável | Para que serve |
|---|---|
| `DATABASE_URL` | Connection string PostgreSQL do Supabase. Use a connection string apropriada ao seu ambiente. |
| `SUPABASE_URL` | URL do projeto Supabase. |
| `SUPABASE_KEY` | Chave publishable para operações de leitura pública. |
| `SUPABASE_SECRET_KEY` | Chave secreta usada pelo servidor para gerenciar integrantes. **Nunca a exponha no navegador.** |
| `SECRET_KEY` | Chave criptográfica do Django. Defina uma chave privada e forte fora do desenvolvimento local. |

No Supabase, os dados do Django usam o schema `django`; o catálogo pode acessar tabelas no schema `public` conforme a configuração atual. As migrations criam/atualizam as tabelas Django:

```bash
python manage.py migrate
```

<details>
<summary><strong>🔑 Checklist antes de iniciar</strong></summary>

- [ ] Copiei `.env.example` para `.env`.
- [ ] Configurei `DATABASE_URL` com acesso PostgreSQL.
- [ ] Preenchi `SUPABASE_URL`, `SUPABASE_KEY` e `SUPABASE_SECRET_KEY`.
- [ ] Mantive `.env` fora do Git.
- [ ] Executei as migrations.

</details>

## 🗺️ Mapa do projeto

```text
DevWeb3/
├── README.md
└── trabalho01/
    ├── manage.py
    ├── requirements.txt
    ├── .env.example
    ├── ap/            # Código legado, não habilitado na configuração atual
    ├── projeto/       # Configurações, rotas globais, layout e arquivos estáticos
    ├── web_site/      # Páginas públicas, equipe e contato
    ├── catalogo/      # Serviços, catálogo e relatórios
    ├── contas/        # Login, cadastro, perfil e recuperação de senha
    ├── login/         # Fluxo legado de autenticação em /login/
    ├── pedidos/       # Carrinho e pedidos
    └── media/          # Imagens enviadas para o catálogo
```

### Apps Django

| App | Responsabilidade |
|---|---|
| `web_site` | Página inicial, “Quem somos”, contato e gestão da equipe. |
| `catalogo` | Serviços, produtos, relatórios e endpoints de categorias. |
| `contas` | Autenticação principal, cadastro, perfil e recuperação de senha. |
| `pedidos` | Carrinho, finalização e histórico de pedidos. |
| `login` | Rotas legadas de autenticação, isoladas no namespace `legacy_login`. |
| `projeto` | Configurações Django, rotas globais, template base e estáticos. |

## 🧭 Rotas úteis

| Endereço | O que abre |
|---|---|
| `/` | Página inicial |
| `/quem-somos/` | Equipe |
| `/produtos/` | Catálogo público |
| `/contato/` | Formulário de contato |
| `/contas/` | Entrar |
| `/contas/cadastro/` | Criar conta |
| `/contas/dashboard/` | Dashboard autenticado |
| `/pedidos/carrinho/` | Carrinho |
| `/pedidos/meus-pedidos/` | Histórico de pedidos |
| `/catalogo/servicos/` | Administração de serviços |
| `/catalogo/relatorios/` | Relatórios |
| `/admin/` | Django Admin |

> As áreas de administração exigem autenticação e permissões adequadas.

## 🧪 Testes

Rode a suíte completa de dentro de `trabalho01`:

```bash
python manage.py test
```

Durante os testes, o projeto configura um banco SQLite em memória; fora deles, exige PostgreSQL.

## 🔒 Segurança e configuração

- **Não** compartilhe nem faça commit do `.env`, senhas, tokens ou chaves privadas.
- `SUPABASE_SECRET_KEY` deve permanecer exclusivamente no servidor.
- O `SECRET_KEY` padrão das configurações é somente um fallback de desenvolvimento. Configure uma chave própria e `DEBUG=False` antes de qualquer implantação.
- O `.env.example` pode ser commitado porque contém apenas nomes e valores fictícios.
- Imagens enviadas pela aplicação ficam em `trabalho01/media/`.

## 🤝 Contribua

1. Faça um fork e crie uma branch para sua alteração.
2. Mantenha as mudanças focadas e siga os padrões do projeto.
3. Execute `python manage.py test`.
4. Abra um pull request descrevendo o problema e a solução.

<details>
<summary><strong>✅ Checklist para pull request</strong></summary>

- [ ] A mudança tem escopo claro.
- [ ] Testes relevantes foram executados.
- [ ] Não há `.env`, credenciais ou arquivos locais no commit.
- [ ] A documentação foi atualizada quando necessário.

</details>

---

<div align="center">

Feito para tirar ideias do papel. ✨

</div>
