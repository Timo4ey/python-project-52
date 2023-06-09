MANAGE := poetry run python manage.py
PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

prod:migrate
	poetry run gunicorn -w 5 task_manager.wsgi

test-django:lint
	 @$(MANAGE)  test task_manager.tests

docker-build:
	docker compose build

up:
	docker compose up

check:
	poetry run pytest task_manager -vv

func-tests:
	 @$(MANAGE) test task_manager.functional_tests

cov:
	poetry run pytest --cov=task_manager

tests-coverage:
	poetry run pytest --cov=task_manager --cov-report xml
lint:
	poetry run flake8 task_manager

.PHONY: install

black:
	poetry run black .

pep-isort:
	poetry run isort . 

mypy:
	poetry run mypy . 

install:
	poetry install

dev:
	poetry run python manage.py runserver

.PHONY: shell
shell:
	@$(MANAGE) shell_plus --ipython

migrate:
	@$(MANAGE) migrate

makemigrations:
	@$(MANAGE) makemigrations

messages:
	@$(MANAGE) makemessages -l en

compilemessages:
	@$(MANAGE) compilemessages

.PHONY: setup
setup: db-clean install migrate

.PHONY: db-clean
db-clean:
	@rm db.sqlite3 || true

syncdb:
	@$(MANAGE) migrate --run-syncdb

build:
	poetry build

publish:
	poetry publish --dry-run

collectstatic:
	poetry run python manage.py collectstatic --noinput