##

publish_to_pip:
	python3 -m pip install --upgrade build twine
    python3 -m build
    python -m twine upload dist/*

publish_to_pypi_test:
	python3 -m pip install --upgrade build twine
    python3 -m build
    python3 -m twine upload  --skip-existing --repository testpypi dist/*