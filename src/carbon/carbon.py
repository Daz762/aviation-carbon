import click
from carbon.actions.apikey import action_key
from carbon.actions.airports import action_airports
from carbon.actions.single import action_single
from carbon.actions.multi import action_multi


@click.group()
def cli():
    pass


@click.command(help="add api key")
@click.option("-k", "--key", type=str, help="add your carbon api key")
def key(key):
    action_key(key)


@click.command(help="list all airports and correspondng codes")
@click.option("-s", "--search", type=str, help="search for an airport. refines returned results")
def airports(search):
    action_airports(search)


@click.group(help="calculate carbon footprint for a single or multi leg journey")
def footprint():
    pass


@footprint.command("single", help="calcualte carbon footprint for a single journey")
@click.option("-d", "--departure", type=str, help="departure airport code")
@click.option("-a", "--arrival", type=str, help="arrival airport code")
@click.option("-c", "--cabin", type=str, default="e", help="cabin class")
@click.option("-p", "--passengers", type=int, default=1, help="number of passengers")
def single(departure, arrival, cabin, passengers):
    action_single(departure, arrival, cabin, passengers)


@footprint.command("multi", help="calcualte carbon footprint for a multi leg journey")
@click.option("-a", "--airports", type=str, help="list of airports in order of travel E.G. LHR,HND,LAX")
@click.option("-c", "--cabin", type=str,help="list of cabin classes in order of travel (excluding final destination) E.G. P,F")
@click.option("-p", "--passengers", type=int, default=1, help="number of passengers")
def multi(airports, cabin, passengers):
    action_multi(airports, cabin, passengers)


cli.add_command(key)
cli.add_command(airports)
cli.add_command(footprint)

if __name__ == '__main__':
    cli()
