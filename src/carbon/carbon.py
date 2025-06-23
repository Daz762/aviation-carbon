import click
from carbon.actions.apikey import action_key
from carbon.actions.airports import action_airport_search
from carbon.actions.singleleg import action_singleleg
from carbon.actions.multileg import action_multileg

AIRPORT_SEARCH = "https://sharpapi.com/api/v1/airports"
CARBON_ESTIMATE = "https://www.carboninterface.com/api/v1/estimates"

@click.group()
def cli():
    pass


@click.command(help="register an api key with the cli")
@click.option("-c", "--carboninterface", type=str, help="add your carbon interface api key")
@click.option("-s", "--sharpapi", type=str, help="add your sharpapi api key")
def key(carboninterface, sharpapi):
    message = action_key(carboninterface, sharpapi)
    click.echo(message)


@click.group(help="find information on airports")
def airport():
    pass


@airport.command("search", help="search for airports. At least one filter is required to refine results")
@click.option("-c", "--city", type=str, help="filter by city. partial entries allowed")
@click.option("-co", "--country", type=str, help="filter by 2 letter country code. E.G GB. partial entries not allowed")
@click.option("-n", "--name", type=str, help="filter by airport name. partial entries allowed")
def search(city, country, name):
    message = action_airport_search(AIRPORT_SEARCH, city, country, name)
    click.echo(message)


@click.group(help="calculate carbon footprint for a single or multi leg journey")
def footprint():
    pass


@footprint.command("singleleg", help="calcualte carbon footprint for a single journey")
@click.option("-d", "--departure", type=str, help="departure airport code")
@click.option("-a", "--arrival", type=str, help="arrival airport code")
@click.option("-c", "--cabin", type=str, default="e", help="cabin class. e(conomy) or p(remium)")
@click.option("-p", "--passengers", type=int, default=1, help="number of passengers")
@click.option("-tu", "--tunit", type=str, default="k", help="distance travelled unit. m(iles) or k(ilometers)")
@click.option("-ru", "--runit", type=str, default="kg", help="emmisions unit. g(rams), l(bs), k(g) or m(t)")
def singleleg(departure, arrival, cabin, passengers, tunit, runit):
    message = action_singleleg(CARBON_ESTIMATE, departure, arrival, cabin, passengers, tunit, runit)
    click.echo(message)

@footprint.command("multileg", help="calculate carbon footprint for a multi leg journey")
@click.option("-l", "--legs", type=str, help="leg in format of DEP,ARR,CAB (E.G LGW,HND,P). option can be used multiple times to calculate mutliple legs", multiple=True)
@click.option("-p", "--passengers", type=int, default=1, help="number of passengers")
@click.option("-c", "--cabin", type=str, default="e", help="cabin class. e(conomy) or p(remium)")
def multileg(leg, passengers):
    message = action_multileg(leg, passengers)
    click.echo(message)


cli.add_command(key)
cli.add_command(airport)
cli.add_command(footprint)

if __name__ == '__main__':
    cli()
