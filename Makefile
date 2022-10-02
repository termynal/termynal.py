.DEFAULT_GOAL := help
CODE = termynal tests
POETRY_RUN = poetry run
TEST = $(POETRY_RUN) pytest $(args)

.PHONY: help
help: ## Show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: format lint test  ## Run format lint test

.PHONY: lock
lock:  ## Lock dependencies
	poetry lock

.PHONY: update
update:  ## Update dependencies
	poetry update

.PHONY: build
build:  ## Build package
	poetry build

.PHONY: install
install:  ## Install dependencies
	poetry install

.PHONY: publish
publish:  ## Publish package
	@poetry publish --build --no-interaction --username=$(pypi_username) --password=$(pypi_password)

.PHONY: test
test:  ## Test with coverage
	$(TEST) --cov

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
	$(POETRY_RUN) flake8 --jobs 1 --statistics --show-source $(CODE)
	$(POETRY_RUN) pylint --jobs 1 --rcfile=pyproject.toml $(CODE)
	$(POETRY_RUN) bandit -c pyproject.toml -r $(CODE)
	$(POETRY_RUN) black --check $(CODE)
	$(POETRY_RUN) pytest --dead-fixtures --dup-fixtures
	$(POETRY_RUN) mypy $(CODE)

.PHONY: format
format:  ## Formating code
	$(POETRY_RUN) autoflake --recursive --in-place --remove-all-unused-imports $(CODE)
	$(POETRY_RUN) isort $(CODE)
	$(POETRY_RUN) black $(CODE)
	$(POETRY_RUN) unify --in-place --recursive $(CODE)

.PHONY: docs
docs:  ## Build docs
	$(POETRY_RUN) mkdocs build -s -v

.PHONY: docs-serve
docs-serve:  ## Serve docs
	$(POETRY_RUN) mkdocs serve

.PHONY: docs-changelog
docs-changelog:  ## Build changelog
	$(POETRY_RUN) git-changelog -s conventional -o CHANGELOG.md .

.PHONY: update-changelog  ## Update changelog (commit)
update-changelog: docs-changelog
	git add .
	git commit -m "docs: update changelog"

.PHONY: bump-version
bump-version:  ## Bump version (commit and tag)
	poetry version $(v)
	git add . && git commit -m "Bump version $(v)"
	git tag -m "" -a $(v)
	make update-changelog

.PHONY: clean
clean:  ## Clean
	rm -rf site || true
	rm -rf dist || true
	rm -rf htmlcov || true

.PHONY: git-lint
git-lint:  ## Check git commit
	$(POETRY_RUN) gitlint
