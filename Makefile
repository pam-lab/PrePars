.ONESHELL:

SHELL=/bin/bash

.PHONY:help
help:
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'

clean: ## cleans generated files
	rm -rf src/prepars.egg-info
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf tests/__pycache__

publish_to_pip: clean ## publish this package to pip
	python3 -m pip install --upgrade build twine
	python3 -m build
	python -m twine upload dist/*

publish_to_pypi_test: clean ## publish this package to pypi
	python3 -m pip install --upgrade build twine
	python3 -m build
	python3 -m twine upload --repository testpypi dist/*

PVC.zip: 
	pip install gdown
	gdown 1aIDGD3hHjDyWZ5i8vmgtMxRAzSxGFCWY 

download_all_verbs: PVC.zip
	./download.sh

run_tests: ## run all tests
	pip install pytest
	pip install .
	pytest

build_docs: ## build complete sphinx documentation from source files
	# https://brendanhasz.github.io/2019/01/05/sphinx.html
	pip install sphinx
	sphinx-apidoc -o docs/source src/prepars
	cd docs
	make clean
	make html