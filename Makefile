.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

TEST_SESSIONS := $(shell nox --json -l | jq -r '.[] | select(.session | startswith("test")) | .session' | tr "\t" " ")
NOX_CMD := pdm run nox -r

.PHONY: install
install: ## setup environment
	pdm venv create

.PHONY: build
build: ## build source distribution and wheel package
	pdm build --clean

.PHONY: lint
lint: ## check style with flake8
	$(NOX_CMD) --tags lint

.PHONY: test
test: ## run tests
	$(NOX_CMD) --session $(TEST_SESSIONS)

.PHONY: release-test
release-test: ## release packages to testpypi server
	pdm publish --repository testpypi

.PHONY: release-prod
release-prod: ## release packages to pypi server
	pdm publish

.PHONY: dist-clean
dist-clean: ## remove build artifacts
	@-rm -f dist/*

.PHONY: clean
clean: ## clean up all artifacts
	git clean -fdx
