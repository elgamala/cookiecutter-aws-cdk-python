.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint: ## check style with flake8
	flake8 {{ cookiecutter.project_slug }} tests

test: ## run tests quickly with the default Python
	pytest -v

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source {{ cookiecutter.project_slug }} -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/{{ cookiecutter.project_slug }}.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ {{ cookiecutter.project_slug }}
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	pip3 install -r requirements_dev.txt -r requirements.txt


all bootstrap deploy diff destroy: check-credentials

bootstrap: qualifier 			:= $(shell cat cdk.json | jq -r '.context."@aws-cdk/core:bootstrapQualifier"')
bootstrap: main_account 		:= $(shell cat cdk.json | jq -r '.context.environments.master.account')
bootstrap: main_region 			:= $(shell cat cdk.json | jq -r '.context.environments.master.region')
bootstrap: tooling_account 		:= $(shell cat cdk.json | jq -r '.context.environments.tooling.account')
bootstrap: tooling_region 		:= $(shell cat cdk.json | jq -r '.context.environments.tooling.region')
bootstrap: dr_account 			:= $(shell cat cdk.json | jq -r '.context.environments.disasterRecovery.account')
bootstrap: dr_region 			:= $(shell cat cdk.json | jq -r '.context.environments.disasterRecovery.region')

check-credentials:
	@echo 'Checking AWS Credentials'
	aws sts get-caller-identity

ls synth diff deploy destroy:
	@echo "\033[92mRunning CDK $@ $(filter-out $@,$(MAKECMDGOALS))\033[0m"
	@cdk $@ --all --require-approval never --progress events
bootstrap:
	@$(MAKE) bootstrap-environment account=$(main_account) region=$(main_region) qualifier=${qualifier}
	@$(MAKE) bootstrap-environment account=$(tooling_account) region=$(tooling_region) qualifier=${qualifier}
	@$(MAKE) bootstrap-environment account=$(dr_account) region=$(dr_region) qualifier=${qualifier}

bootstrap-environment:
	@echo "\033[92mRunning CDK bootstrap aws://$(account)/$(region)\033[0m"
	@aws cloudformation deploy \
		--stack-name 'CDKToolkit' \
		--template-file prerequisites/cdk-bootstrap.yaml \
		--parameter-overrides "Qualifier=$(qualifier)" \
		--no-fail-on-empty-changeset \
		--capabilities CAPABILITY_NAMED_IAM \
		--region "$(region)"

	@aws cloudformation describe-stack-events \
		--stack-name 'CDKToolkit' \
		--region "$(region)"

security-checks:
	@cdk synth
	@docker-compose up --abort-on-container-exit
	@checkov -d . --config-file checkov.yaml
