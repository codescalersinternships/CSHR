
CMD:=poetry run

install:
	poetry update
	poetry install
	poetry check




lint:
	$(CMD) flake8 .  --exclude=__init__.py


migrate:
	$(CMD) python3 manage.py makemigrations
	$(CMD) python3 manage.py migrate
	$(CMD) python3 manage.py sqlmigrate cshr 0006