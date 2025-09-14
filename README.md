# Member Book Service

API para gerenciamento de membros e empresas construída com FastAPI, SQLAlchemy e Alembic.

## 🚀 Características

- **FastAPI**: Framework moderno e rápido para APIs
- **SQLAlchemy**: ORM para Python
- **Alembic**: Sistema de migrações
- **Poetry**: Gerenciamento de dependências
- **PostgreSQL**: Banco de dados

## 📋 Pré-requisitos

- Python 3.9+
- Poetry
- PostgreSQL

## 🛠️ Instalação

### Opção 1: Docker (Recomendado)

1. Clone o repositório:
```bash
cd /home/$(whoami)/Documents/member-book-service
```

2. Execute o setup completo:
```bash
make setup
```

Isso irá:
- Construir a imagem Docker
- Subir os containers (app + PostgreSQL)
- Executar as migrações
- Popular dados iniciais

### Opção 2: Instalação Local

1. Instale as dependências:
```bash
poetry install
```

2. Configure o banco de dados:
```bash
# Crie o banco de dados PostgreSQL
createdb member_book_db

# Configure as variáveis de ambiente (copie o arquivo de exemplo)
cp env.example .env
# Edite o arquivo .env com suas configurações de banco
```

3. Execute as migrações:
```bash
# Usando o script
./migrate.py

# Ou manualmente
poetry run alembic upgrade head
```

4. Execute a aplicação:
```bash
# Usando o script
./run.py

# Ou manualmente
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🐳 Comandos Docker

```bash
# Ver todos os comandos disponíveis
make help

# Subir a aplicação
make up

# Parar a aplicação
make down

# Ver logs
make logs

# Executar migrações
make migrate

# Popular dados iniciais
make seed

# Testar API
make test-api

# Status dos containers
make status
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação da API

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔗 Endpoints Principais

### Health Check
- `GET /health` - Verificar status da API

### Members
- `PUT /members-book-service/v1/members/populate-data` - Popular dados iniciais (profiles)

## 🗃️ Estrutura do Banco de Dados

O projeto inclui as seguintes tabelas:

- **profiles** - Tipos de perfis de usuário
- **addresses** - Endereços
- **market_segmentation** - Segmentação de mercado
- **companies** - Empresas
- **members** - Membros
- **contact_channels** - Canais de contato
- **additional_infos** - Informações adicionais dos membros
- **performance** - Performance das empresas
- **performance_events** - Eventos de performance
- **members_companies** - Relacionamento membros-empresas

## 🌱 Seed de Dados

O endpoint `/members-book-service/v1/members/populate-data` popula automaticamente a tabela `profiles` com os seguintes tipos:

1. **eternity** - Acesso completo e vitalício
2. **infinity** - Acesso premium com recursos avançados
3. **admin** - Acesso administrativo completo
4. **standalone_profile** - Acesso individual com prazo de expiração

## 🧪 Testando a API

```bash
# Testar health check
curl http://localhost:8000/health

# Popular dados iniciais
curl -X PUT http://localhost:8000/members-book-service/v1/members/populate-data
```

## 📁 Estrutura do Projeto

```
member-book-service/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       └── api.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── address.py
│   │   ├── company.py
│   │   ├── contact_channel.py
│   │   ├── market_segmentation.py
│   │   ├── member.py
│   │   ├── member_company.py
│   │   ├── performance.py
│   │   ├── performance_event.py
│   │   ├── profile.py
│   │   └── additional_info.py
│   ├── seeds/
│   │   └── profiles_seed.py
│   └── main.py
├── alembic/
│   └── versions/
├── pyproject.toml
├── alembic.ini
├── run.py
├── migrate.py
└── README.md
```
