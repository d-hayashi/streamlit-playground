#
# Makefile
#

VERSION ?= $(shell ./utils/get_version.sh)
COMMIT_ID := $(shell git rev-parse HEAD)

IMAGE_PREFIX ?= registry.gitlab.com/hdwlab
IMAGE_NAME ?= $(shell basename ${PWD})
$(warning Image: $(IMAGE_PREFIX)/$(IMAGE_NAME):$(VERSION))

help: ## Show this help
	@echo "Help"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "    \033[36m%-20s\033[93m %s\n", $$1, $$2}'

.PHONY: default
default: help

.PHONY: build-image
build-image:	## Build an image
	DOCKER_BUILDKIT=1 docker build -t $(IMAGE_PREFIX)/$(IMAGE_NAME):$(VERSION) .

.PHONY: publish-image
publish-image:    ## Publish an image
	docker push $(IMAGE_PREFIX)/$(IMAGE_NAME):$(VERSION)

.PHONY: run-image
run-image:    ## Run an image
	docker run -it --rm $(IMAGE_PREFIX)/$(IMAGE_NAME):$(VERSION)

.venv:
	poetry config virtualenvs.create true --local
	poetry config virtualenvs.in-project true --local
	poetry install

install: .venv

.PHONY: lint
lint: .venv		## Run pflake8
	poetry run pflake8 && poetry run black . --check --diff

.PHONY: test
test: .venv		## Run pytest
	poetry run pytest test

.PHONY: format
format: .venv	## Run black
	poetry run black .
