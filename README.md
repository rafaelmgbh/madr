# Projeto MADR (Mader)



## Visão Geral

O **MADR** é uma API desenvolvida com FastAPI para gerenciar um acervo digital de romances. Ela permite operações de CRUD (criar, ler, atualizar e deletar) para livros e romancistas, além de incluir o registro de contas e autenticação para operações específicas.
No projeto cada usuário possui uma conta (protegida pro e-mail/senha). Depois que está "dentro" da conta (ou seja, authenticado com um JWT), o usuário pode criar/ler/atualizar/excluir romancistas e livros que queira guardar no acervo.
<h2 id="stack">Tecnologias Utilizadas</h2>

- Python
- PostgreSQL
- FastAPI
- SQLAlchemy
- Alembic
- Pytest

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/rafaelmgbh/madr.git
```
```bash
Vá para o diretório da aplicação:
cd madr
```

2. Crie um ambiente virtual com o Poetry:

```
poetry shell
```

3. Instale as dependências do projeto:

```
poetry install
```

##  Uso
O Taskipy é uma biblioteca Python que facilita a criação e execução de tarefas de automação.
Neste projeto usei o [Taskipy](https://pypi.org/project/taskipy/)

```
No console da aplicação execute o comando:
task --list
```
Vai listar todos os comandos disponíveis para Executar, Formatar e Testar a aplicação:
```
lint           ruff check .; ruff check . --diff
format         ruff check . --fix; ruff format .
pre_test       task lint
test           pytest -s -x --cov=madr -vv
post_test      coverage html
run            fastapi dev madr/app.py
auto_migration alembic revision --autogenerate -m
migration_up   alembic upgrade head
migration_down alembic downgrade -1
```

Executa o projeto:
```bash
task run
```

Abra o seu navegador, a aplicação estará disponível para ser executada no endereço local: `http://127.0.0.1:8000/docs`.
