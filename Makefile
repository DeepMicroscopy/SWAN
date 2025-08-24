SHELL := /bin/bash

default: all
all: frontend backend

frontend: backend-api
	$(MAKE) -C frontend all build

backend: frontend
	$(MAKE) -C backend all build

backend-api:
	$(MAKE) -C backend api

.PHONY: all frontend backend backend-api

.PHONY: dev
dev:
	$(MAKE) -j2 _dev

.PHONY: _dev
_dev: dev-frontend dev-backend

.PHONY: dev-frontend
dev-frontend:
	$(MAKE) -C frontend dev

.PHONY: dev-backend
dev-backend:
	$(MAKE) -C backend dev

.PHONY: run
run:
	$(MAKE) -C backend run