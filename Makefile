.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: clean
clean: ## clean up all artifacts
	git clean -fdx

.PHONY: dist-clean
dist-clean: ## remove build artifacts
	-rm -fr build dist .eggs
	-find . -name '*.egg' \
		-o -name '*.egg-info' \
		-print0 | xargs -0 rm -fr

lint: ## check style with flake8
	hatch run lint:full

test: ## run tests
	hatch run test:term

dist: ## build source distribution and wheel package
	hatch build --clean

release-test: ## release packages to testpypi server
	twine upload -r testpypi dist/*

release-prod: ## release packages to pypi server
	twine upload -r pypi dist/*

install: ## setup environment
	hatch env create
