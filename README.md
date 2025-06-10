# aviation-carbon
A CLI to show you your carbon footprint for a flight

## Spec

Things that the CLI needs to do:

- [x] add api key
- [ ] get list of airport codes
- [ ] calculate footprint (cabin class etc)
- [ ] test suite
- [ ] docker image
- [ ] makefile
- [ ] readme (install dependencies)

## Accounts needed
carbon interface: https://docs.carboninterface.com/#/
airports database: http://sharpapi.com/en/catalog/utility/airports-database-flight-duration-calculator

## build locally 

```shell
pip install -e .
```

## Virtual Environment Stuff

```shell
# create virtual environment
python -m venv .venv

# activate virtual environment
source ./.venv/bin/activate

# save sources
pip freeze > requirements.txt
```