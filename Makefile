PORT ?= 8000
start:
	poetry run gunicorn -w 5 task_manager.wsgi

test-django:lint
	 poetry run python manage.py test task_manager/tests

lint:
	flake8 task_manager