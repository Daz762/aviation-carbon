import click
from carbon.actions.apikey import action_key
from carbon.actions.airports import action_airports
from carbon.actions.singleleg import action_singleleg
from carbon.actions.multileg import action_multileg


@click.group()
def cli():
    pass


@click.command(help="add api key")
@click.option("-c", "--carbon", type=str, help="add your carbon interface api key")
@click.option("-a", "--airport", type=str, help="add your airport database api key")
def key(carbon, airport):
    action_key(carbon, airport)


@click.command(help="list all airports and correspondng codes")
@click.option("-s", "--search", type=str, help="search for an airport. refines returned results")
def airports(search):
    action_airports(search)


@click.group(help="calculate carbon footprint for a single or multi leg journey")
def footprint():
    pass


@footprint.command("singleleg", help="calcualte carbon footprint for a single journey")
@click.option("-d", "--departure", type=str, help="departure airport code")
@click.option("-a", "--arrival", type=str, help="arrival airport code")
@click.option("-c", "--cabin", type=str, default="e", help="cabin class. e(conomy) or p(remium)")
@click.option("-p", "--passengers", type=int, default=1, help="number of passengers")
def singleleg(departure, arrival, cabin, passengers):
    action_singleleg(departure, arrival, cabin, passengers)


@footprint.command("multileg", help="calculate carbon footprint for a multi leg journey")
@click.option("-l", "--leg", type=str, help="leg in format of DEP,ARR,CAB (E.G LGW,HND,P). option can be used multiple times to calculate mutliple legs", multiple=True)
@click.option("-p", "--passengers", type=int, default=1, help="number of passengers")
def multileg(leg, passengers):
    action_multileg(leg, passengers)


cli.add_command(key)
cli.add_command(airports)
cli.add_command(footprint)

if __name__ == '__main__':
    cli()
