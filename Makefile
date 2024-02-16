.PHONY: setup test clean

setup:
	python3 -m venv venv &&\
	. venv/bin/activate &&\
	pip install --upgrade pip setuptools &&\
	pip install -r requirements.txt -r requirements-dev.txt -r requirements-docs.txt &&\
	python -m pip install -e .

setup-test-unit:
	python -m venv venv &&\
	. venv/bin/activate &&\
	pip install -r requirements.txt -r requirements-dev.txt &&\
	python -m pip install -e .

test:
	python -m coverage run --source regex_rename -m pytest -vv --tb=short -ra --color=yes $(test)
	python -m coverage report --show-missing --skip-empty --skip-covered

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf ./*.egg-info

# use token from .pypirc
release: clean
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload -u __token__ dist/*

mkdocs-local:
	mkdocs serve

mkdocs-push:
	mkdocs gh-deploy --force --clean --verbose
