setup:
	python3 -m venv ~/.continuous-integration

install:
	pip install -r requirements.txt

test: 
	python -m pytest -vv --cov=repolib tests/*.py

lint:
	pylint --disable=R.C repolib

all: install lint test
