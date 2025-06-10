build:
	pip install .

build-editable:
	pip install -e .

test:
	python -m unittest discover tests