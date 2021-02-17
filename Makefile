.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' \
	| sort

.PHONY: clean
clean: clean-build clean-pyc clean-test ## clean up all artifacts

.PHONY: clean-build
clean-build: ## remove build artifacts
	-rm -fr build dist .eggs
	-find . -name '*.egg' \
		-o -name '*.egg-info' \
		-print0 | xargs -0 rm -fr

.PHONY: clean-pyc
clean-pyc: ## remove Python intermediate files
	-find . -name '*.pyc' \
		-o -name '*.pyo' \
		-o -name '*~' \
		-o -name '__pycache__' \
		-print0 | xargs -0 rm -fr

.PHONY: clean-test
clean-test: ## remove unittest related artifacts
	-rm -fr .tox .coverage htmlcov .pytest_cache .mypy_cache

lint: ## check style with flake8
	@flake8 drf_renderer_svgheatmap tests

test: ## run tests
	@python -m pytest

test-lint: ## run lint related tests
	@tox -e flake8,isort

test-all: ## run all tests with tox
	@tox

dist: ## build source distribution and wheel package
	@python setup.py sdist bdist_wheel
	@ls -l dist

release-test: ## release packages to testpypi server
	twine upload -r testpypi dist/*

release-prod: ## release packages to pypi server
	twine upload -r pypi dist/*

install:
	python setup.py install
