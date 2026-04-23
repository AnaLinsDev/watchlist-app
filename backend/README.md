# Watchlist API (FastAPI + SQLAlchemy + Alembic)

API para gerenciamento de watchlists (filmes/séries), construída com FastAPI, SQLAlchemy e Alembic.

---

## 📦 Requisitos

* Python 3.10+
* pip
* (Opcional) PostgreSQL

---

## 🚀 Setup do projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/AnaLinsDev/watchlist-app.git
cd watchlist-app/backend
```

---

### 2. Criar ambiente virtual (venv)

```bash
python -m venv venv
```

Ativar:

* Windows (CMD):

```bash
venv\Scripts\activate
```

* Windows (PowerShell):

```bash
venv\Scripts\Activate.ps1
```

* Linux / macOS:

```bash
source venv/bin/activate
```

---

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=sqlite:///./test.db
```

### Exemplo com PostgreSQL

```env
DATABASE_URL=postgresql://user:password@localhost:5432/watchlist_db
```

---

## Rodar a aplicação

```bash
uvicorn app.main:app --reload
```

A API estará disponível em:

* http://localhost:8000
* Docs: http://localhost:8000/docs

---

## Banco de dados e migrations (Alembic)

### Criar uma nova migration

Sempre que alterar os models:

```bash
alembic revision --autogenerate -m "description of changes"
```

---

### Revisar a migration

Antes de aplicar, abra o arquivo gerado em:

```bash
alembic/versions/
```

Verifique:

* tabelas criadas corretamente
* foreign keys
* tipos de dados

---

### Aplicar migration

```bash
alembic upgrade head
```

---

### Reverter migration

```bash
alembic downgrade -1
```

---

## Fluxo de desenvolvimento

1. Criar/alterar models
2. Gerar migration
3. Revisar arquivo
4. Rodar `upgrade`
