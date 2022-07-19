
.PHONY: init
init:
	pip install -r requirements.txt

.PHONY: setup-develop
setup-develop:
	pip install -e .'[dev]'
	pre-commit install

.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files

.PHONY: lint
lint:
	flake8 . --count --statistics --exit-zero
	python -m pylint .

.PHONY: test
test:
	pytest -v .
