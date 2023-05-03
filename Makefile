MANAGE := poetry run python manage.py

start:
	poetry run gunicorn -w 5 task_manager.wsgi

test-django:lint
	 poetry run python manage.py test task_manager/tests

lint:
	poetry run flake8 task_manager

.PHONY: install
install:
	poetry install

dev:
	poetry run python manage.py runserver

.PHONY: shell
shell:
	@$(MANAGE) shell_plus --ipython

migrate:
	@$(MANAGE) migrate

messages:
	@$(MANAGE) makemessages -l en

compilemessages:messages
	@$(MANAGE) compilemessages

.PHONY: setup
setup: db-clean install migrate

.PHONY: db-clean
db-clean:
	@rm db.sqlite3 || true


