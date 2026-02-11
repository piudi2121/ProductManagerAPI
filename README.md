
---

# Product Manager API

API REST simples para gerenciamento de produtos, desenvolvida com **FastAPI**, **SQLAlchemy** e **SQLite**, com foco em aprendizado de backend e boas práticas básicas.

## Funcionalidades

* Criar produtos
* Listar todos os produtos
* Buscar produto por ID
* Atualizar produto
* Deletar produto
* Filtrar produtos por categoria

## Tecnologias utilizadas

* Python 3.10+
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic

## Estrutura do produto

Um produto possui os seguintes campos:

* `id` (int)
* `name` (string, único)
* `desc` (string)
* `stock` (int)
* `price` (decimal)
* `category` (string)
* `created_at` (datetime)
* `updated_at` (datetime)

## Como rodar o projeto

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

2. Instale os pacotes necessários:

```bash
pip install fastapi uvicorn sqlalchemy
```

3. Inicie o servidor:

```bash
uvicorn main:app --reload
```

4. Acesse a documentação interativa:

* Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Endpoints principais

* `POST /products` – Criar produto
* `GET /products` – Listar produtos
* `GET /products/{id}` – Buscar produto por ID
* `PUT /products/{id}` – Atualizar produto
* `DELETE /products/{id}` – Remover produto

## Observações

* O banco de dados é criado automaticamente usando SQLite
* Projeto voltado para estudo e prática de FastAPI + SQLAlchemy
* Não utiliza migrations (Alembic) por simplicidade

---