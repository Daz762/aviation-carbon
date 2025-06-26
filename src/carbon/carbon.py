import click
from carbon.airports.airports import action_airport_search
from carbon.apikeys.apikey import action_key, read_key
from carbon.travel.multileg import action_multileg
from carbon.travel.singleleg import action_singleleg

AIRPORT_SEARCH = "https://sharpapi.com/api/v1/airports"
CARBON_ESTIMATE = "https://www.carboninterface.com/api/v1/estimates"

@click.group()
def cli():
    pass


@click.command(help="\b\nregister an api key with the cli")
@click.option("-c", "--carboninterface", type=str, help="\b\nadd your carbon interface api key")
@click.option("-s", "--sharpapi", type=str, help="\b\nadd your sharpapi api key")
def key(carboninterface, sharpapi):
    message = action_key(carboninterface, sharpapi)
    click.echo(message)


@click.group(help="find information on airports")
def airport():
    pass


@airport.command("search", help="\b\nsearch for airports. At least one filter is required to refine results")
@click.option("-c", "--city", type=str, help="\b\nfilter by city. partial entries allowed")
@click.option("-co", "--country", type=str, help="\b\nfilter by 2 letter country code. E.G GB. partial entries not allowed")
@click.option("-n", "--name", type=str, help="\b\nfilter by airport name. partial entries allowed")
def search(city, country, name):
    apikey = read_key("sharpapi")
    message = action_airport_search(AIRPORT_SEARCH, apikey, city, country, name)
    click.echo(message)


@click.group(help="calculate carbon footprint for a single or multi leg journey")
def footprint():
    pass


@footprint.command("singleleg", help="\b\ncalcualte carbon footprint for a single journey")
@click.option("-d", "--departure", type=str, help="\b\ndeparture airport code. required")
@click.option("-a", "--arrival", type=str, help="\b\narrival airport code. required")
@click.option("-c", "--cabin", type=str, default="e", help="\b\ncabin class. e(conomy) or p(remium). default e")
@click.option("-p", "--passengers", type=int, default=1, help="\b\nnumber of passengers. default 1")
@click.option("-du", "--dunit", type=str, default="km", help="\b\ndistance travelled unit. mi(les) or km. default km")
@click.option("-eu", "--eunit", type=str, default="k", help="\b\nemmisions unit. g(rams), l(bs), k(g) or m(t). default k")
def singleleg(departure, arrival, cabin, passengers, dunit, eunit):
    apikey = read_key("carbon")
    message = action_singleleg(CARBON_ESTIMATE, apikey, departure, arrival, cabin, passengers, dunit, eunit)
    click.echo(message)

@footprint.command("multileg", help="\b\ncalculate carbon footprint for a multi leg journey")
@click.option("-l", "--leg", type=str,
              help="\b\nleg in format of DEP,ARR,CAB (E.G LGW,HND,P). required. option can be used multiple times to calculate mutliple legs",
              multiple=True)
@click.option("-p", "--passengers", type=int, default=1, help="\b\nnumber of passengers. default 1")
@click.option("-du", "--dunit", type=str, default="km", help="\b\ndistance travelled unit. mi(les) or km. default km")
@click.option("-eu", "--eunit", type=str, default="k",
              help="\b\nemmisions unit. g(rams), l(bs), k(g) or m(t). default k")
def multileg(leg, passengers, dunit, eunit):
    apikey = read_key("carbon")
    message = action_multileg(CARBON_ESTIMATE, apikey, leg, passengers, dunit, eunit)
    click.echo(message)


cli.add_command(key)
cli.add_command(airport)
cli.add_command(footprint)

if __name__ == '__main__':
    cli()
