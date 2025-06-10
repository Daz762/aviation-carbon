build:
	python -m unittest discover tests
	pip install .

build-e:
	python -m unittest discover tests
	pip install -e .

test:
	python -m unittest discover tests