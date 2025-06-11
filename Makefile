# builds non editable package
build:
	python -m unittest discover tests
	pip install .

# build editable package - use this for active development
build-e:
	python -m unittest discover tests
	pip install -e .

# run test suite
test:
	python -m unittest discover tests

# build docker image
# Todo