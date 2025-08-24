SHELL := /bin/bash

default: all

.PHONY: all
all: install api check-dev

.PHONY: install
install: node_modules/
node_modules/:
	yarn install -A

.PHONY: api
api:
	yarn run api

.PHONY: check-dev
check-dev:
	yarn check
	yarn run lint
	yarn run test:ts

.PHONY: check
check: check-dev
	yarn run type-check

.PHONY: dev
dev:
	yarn run dev

.PHONY: run
run:
	yarn run preview

.PHONY: build
build: check
	yarn run build