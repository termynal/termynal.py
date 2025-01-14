.DEFAULT_GOAL := help
CODE = termynal tests
RUNNER = uv run
TEST = $(RUNNER) pytest $(args)

.PHONY: help
help: ## Show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: format lint test  ## Run format lint test

.PHONY: install-uv
install-uv:  ## Install uv
	pip install uv

.PHONY: install
install:  ## Install dependencies
	uv sync --all-extras

.PHONY: install
update-deps:  ## Update dependencies
	uv sync --all-extras -U

.PHONY: install-docs
install-docs:  ## Install docs dependencies
	uv sync --group docs

.PHONY: install-git
install-git:  ## Install git dependencies
	uv sync --group git

.PHONY: build
build:  ## Build package
	@uv build --no-progress --no-sources

.PHONY: publish
publish: build  ## Publish package
	@uv publish --username=$(pypi_username) --password=$(pypi_password)

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
	$(RUNNER) python -m webbrowser 'htmlcov/index.html'

.PHONY: lint
lint:  ## Check code
	$(RUNNER) ruff check $(CODE)
	$(RUNNER) pytest --dead-fixtures --dup-fixtures
	$(RUNNER) mypy $(CODE)

.PHONY: format
format:  ## Formatting code
	$(RUNNER) ruff format $(CODE)

.PHONY: docs
docs:  ## Build docs
	$(RUNNER) mkdocs build -s -v

.PHONY: docs-serve
docs-serve:  ## Serve docs
	$(RUNNER) mkdocs serve

.PHONY: bump
bump:  ## Bump version (commit and tag)
	$(RUNNER) cz bump --major-version-zero

.PHONY: clean
clean:  ## Clean
	rm -rf site || true
	rm -rf dist || true
	rm -rf htmlcov || true
