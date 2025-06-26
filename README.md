# aviation-carbon
A CLI to show you your carbon footprint for a flight

## Examples
```
# single leg journey
carbon footprint singleleg -d LHW -a lgw -p 2 -c e -du mi -eu k
carbon footprint singleleg --departure LHW --arrival lgw --passengers 2 --cabin e --dunit mi --eunit k

# multileg journey
carbon footprint multileg -l LGW,HND,P -l HND,LAX,E -p 2 -du km -eu k
carbon footprint multileg --leg LGW,HND,P --leg HND,LAX,E --passengers 2 --dunit km --eunit k

# airport search
carbon airport search -co NZ -c auck -n auck
carbon airport search --country NZ --city auck --name auck
```

## Spec

Things that the CLI needs to do:

- [x] add api key
- [x] get list of airport codes
- [x] calculate footprint (cabin class etc)
- [x] test suite
- [ ] docker image
- [ ] makefile
- [ ] readme (install dependencies)

## Accounts needed
carbon interface: https://docs.carboninterface.com/#/
sharpapi: http://sharpapi.com/en/

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

pip3 install -r requirement.txt

# save sources
pip freeze > requirements.txt
```