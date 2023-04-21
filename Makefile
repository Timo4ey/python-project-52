PORT ?= 8000
start:
	poetry run python manage.py runserver 0.0.0.0:$(PORT)