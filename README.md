# aviation-carbon

A CLI that can calculate the carbon emissions for a single leg or multi leg aviation journey.

The application has been built with Linux and MacOS systems in mind and therefore steps to set up with Windows may vary slightly. The README aims to make it clear at points when the instructions may be different for Windows.

To ensure the application can be ran on all systems the CLI can also be built as a docker container.

## Pre Requisites

Before you can use the carbon CLI you will need to set up accounts for both carbon interface and sharpapi and create an API key for both

carbon interface: [https://docs.carboninterface.com/#/] - used for the emissions calculations functionality
sharpapi: [http://sharpapi.com/en/] - used for the airport search functionality

Once you have an API key for both of the above you can use the CLI to save the keys. Alternatively you can save them as the following environment variables

`CARBON_INTERFACE` & `SHARPAPI`

## Dev Setup

If you want to contribute to this project you will need to have Python and a few other pre-requisites installed. Follow the instruction below to get set up.

- Install PyEnv: [https://github.com/pyenv/pyenv?tab=readme-ov-file#installation]
- From the root of the repo run `pyenv install`. This will install the version of python declared in `.python-version`
- Run `pyenv local` to set the local python version for the project.
- Run `python -m venv .venv` to create a virtual environment for the project.
- Run `source ./.venv/bin/activate` to activate the virtual environment.
- Run `pip3 install -r requirements.txt` to install project dependencies.
- Run `make build-e` to build an editable version of the project.

once the prject is built you should be able to run the `carbon` command. As the build is an editable version any changes you make to the code will be reflected in the previously built project.

To build a version of the project that cannot be edited run `make build`.

If you make any changes that require new packages, make sure these are saved to the `requirements.txt` file using `pip freeze > requirements.txt`

## building the CLI

To build the CLI follow the instructions in the `Dev Setup` section and build with `make build`.

Once you have built the CLI you can run `ln -s .venv/bin/carbon /usr/local/bin/carbon` to but a link to the CLI in your `PATH` on Mac or Linux.

For Windows systems, replace the destination above for an appropriate location that is in the PATH environment variable.

## CLI Examples

```shell
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

## Build with Docker

To build a docker image containing the CLI simply run `make carbon=KEY sharpapi=KEY docker`

replace the values `KEY` with your API for carbon interface and sharpapi.

## CLI Examples (Docker)

```shell
# single leg journey
docker run aviation-carbon:latest carbon footprint singleleg -d LHW -a lgw -p 2 -c e -du mi -eu k
docker run aviation-carbon:latest carbon footprint singleleg --departure LHW --arrival lgw --passengers 2 --cabin e --dunit mi --eunit k

# multileg journey
docker run aviation-carbon:latest carbon footprint multileg -l LGW,HND,P -l HND,LAX,E -p 2 -du km -eu k
docker run aviation-carbon:latest carbon footprint multileg --leg LGW,HND,P --leg HND,LAX,E --passengers 2 --dunit km --eunit k

# airport search
docker run aviation-carbon:latest carbon airport search -co NZ -c auck -n auck
docker run aviation-carbon:latest carbon airport search --country NZ --city auck --name auck
```

## Testing

Tests can be found in the `./tests` directory. The `Makefile` also includes a shortcut for discovering and executing all unit tests.

To run all unit test, simply run `make tests`.
