.PHONY: init test test-all

init:
	pip install -e .[dev]

test: init
	pytest tests

test-all: init
	tox
