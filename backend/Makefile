SHELL := /bin/bash

VENV := .venv
PIP := $(VENV)/bin/pip
RUFF := $(VENV)/bin/ruff
PYTHON := $(VENV)/bin/python
HYPERCORN := $(VENV)/bin/hypercorn
MANAGE := $(PYTHON) manage.py

default: all

.PHONY: all
all: venv freeze api check-dev

.PHONY: venv
venv: $(VENV)/
$(VENV)/:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

.PHONY: freeze
freeze:
	$(PIP) freeze > requirements.txt

.PHONY: api
api: venv
	$(MANAGE) spectacular --file ../docs/openapi.yaml

.PHONY: check-dev
check-dev: venv
	$(PIP) check
	$(RUFF) check --fix
	$(MANAGE) check

.PHONY: check
check: venv check-dev
	$(MANAGE) check --deploy

.PHONY: dev
dev: venv migrations
	$(MANAGE) runserver

.PHONY: run
run: venv
	$(HYPERCORN) swan.wsgi:application -c hypercorn.toml --access-log - --error-log -

.PHONY: migrations
migrations: venv
	$(MANAGE) makemigrations
	$(MANAGE) migrate

.PHONY: build
build: venv check migrations
	$(MANAGE) collectstatic

.PHONY: admin
admin: venv
	$(MANAGE) createsuperuser --username admin --email admin@localhost

.PHONY: example
example: venv
	$(MANAGE) loaddata data.json