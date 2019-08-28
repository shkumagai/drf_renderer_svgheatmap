.PHONY: clean clean-test clean-build help

PYPI_SERVER = pypitest

help:
	@echo "Use \`make <target>' where <target> is one of"
	@echo "  clean       to remove all build, test, coverages, and Python artifacts"
	@echo "  clean-build to remove build artifacts"
	@echo "  clean-pyc   to remove Python file artifacts"
	@echo "  clean-test  to remove test and coverage artifacts"
	@echo "  lint        to check style with flake8"
	@echo "  test        to run tests instantly with default Python"
	@echo "  test-all    to run tests on all Python versions with tox"
	@echo "  dist        to builds source distribution and wheel package"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -fr {} +
	find . -name '*.pyo' -exec rm -fr {} +
	find . -name '*~' -exec rm -fr {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -fr .coverage
	rm -fr htmlcov

lint:
	@flake8 drf_renderer_svgheatmap tests

test:
	@python -m pytest

test-lint:
	@tox -e flake8,isort

test-all:
	@tox

dist:
	@python setup.py sdist bdist_wheel
	@ls -l dist

release: clean dist
	twine upload -r $(PYPI_SERVER) dist/*

install:
	python setup.py install
