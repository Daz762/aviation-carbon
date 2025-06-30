# builds non editable package
build:
	PYTHONPATH=src \
	python -m unittest discover tests
	pip install .

# build editable package - use this for active development
build-e:
	PYTHONPATH=src \
	python -m unittest discover tests
	pip install -e .

# run test suite
test:
	PYTHONPATH=src \
	python -m unittest discover tests

# build docker image
docker:
	PYTHONPATH=src \
	python -m unittest discover tests
	docker build --build-arg CARBON_INTERFACE=$(carbon_interface) --build-arg SHARPAPI=$(sharpapi) . -t aviation-carbon:latest