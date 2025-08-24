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
api:
	$(MANAGE) spectacular --file ../docs/openapi.yaml

.PHONY: check-dev
check-dev:
	$(PIP) check
	$(RUFF) check --fix
	$(MANAGE) check

.PHONY: check
check: check-dev
	$(MANAGE) check --deploy

.PHONY: dev
dev:
	$(MANAGE) runserver

.PHONY: run
run:
	$(HYPERCORN) swan.wsgi:application -c hypercorn.toml --access-log - --error-log -

.PHONY: build
build: check
	$(MANAGE) makemigrations
	$(MANAGE) migrate
	$(MANAGE) collectstatic