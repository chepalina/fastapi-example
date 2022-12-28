.DEFAULT_GOAL = api

CURRENT_DIRECTORY = $(shell pwd)

# Компоненты
api:
	python manage.py start api


# Миграции
migrations-make:
	python manage.py migrations make $(NAME)

migrations-up:
	python manage.py migrations up

migrations-down:
	python manage.py migrations down


# Тесты, линтеры, форматеры
tests-linters:
	cicd/run_tests_linters.sh

unit-tests:
	pytest ./tests

formatters: black isort

black:
	black ./

isort:
	isort ./
