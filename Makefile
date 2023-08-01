.DEFAULT_GOAL := help
CODE = termynal tests
POETRY_RUN = poetry run
TEST = $(POETRY_RUN) pytest $(args)

.PHONY: help
help: ## Show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: format lint test  ## Run format lint test

.PHONY: install-poetry
install-poetry:  ## Install poetry
	pip install poetry

.PHONY: install
install:  ## Install dependencies
	poetry install

.PHONY: install-docs
install-docs:  ## Install docs dependencies
	poetry install --only docs

.PHONY: install-git
install-git:  ## Install git dependencies
	poetry install --only git

.PHONY: publish
publish:  ## Publish package
	@poetry publish --build --no-interaction --username=$(pypi_username) --password=$(pypi_password)

.PHONY: test
test:  ## Test with coverage
	$(TEST) --cov=./

.PHONY: test-fast
test-fast:  ## Test until error
	$(TEST) --exitfirst

.PHONY: test-failed
test-failed:  ## Test failed
	$(TEST) --last-failed

.PHONY: test-report
test-report:  ## Report testing
	$(TEST) --cov --cov-report html
	$(POETRY_RUN) python -m webbrowser 'htmlcov/index.html'

.PHONY: lint
lint:  ## Check code
	$(POETRY_RUN) ruff $(CODE)
	$(POETRY_RUN) black --check $(CODE)
	$(POETRY_RUN) pytest --dead-fixtures --dup-fixtures
	$(POETRY_RUN) mypy $(CODE)

.PHONY: format
format:  ## Formating code
	$(POETRY_RUN) ruff --fix-only $(CODE)
	$(POETRY_RUN) black $(CODE)

.PHONY: docs
docs:  ## Build docs
	$(POETRY_RUN) mkdocs build -s -v

.PHONY: docs-serve
docs-serve:  ## Serve docs
	$(POETRY_RUN) mkdocs serve

.PHONY: bump
bump:  ## Bump version (commit and tag)
	$(POETRY_RUN) cz bump --major-version-zero

.PHONY: clean
clean:  ## Clean
	rm -rf site || true
	rm -rf dist || true
	rm -rf htmlcov || true
