.PHONY: setup test clean

setup:
	python3 -m venv venv &&\
	. venv/bin/activate &&\
	pip install --upgrade pip setuptools &&\
	pip install -r requirements.txt -r requirements-dev.txt &&\
	python setup.py develop

test:
	python3 -m coverage run --source regex_rename -m pytest -vv --tb=short -ra --color=yes $(test)
	python3 -m coverage report --show-missing --skip-empty --skip-covered

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf ./*.egg-info

release-pypi: clean readme
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*
