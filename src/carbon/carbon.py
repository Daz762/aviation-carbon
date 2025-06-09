import click

from carbon.actions.add import command_add
from carbon.actions.greet import command_greet

@click.group()
def cli():
    pass

@click.command(help="greet a person")
@click.option("--name")
def greet(name):
    command_greet(name)

@click.command(help="add a comma seperated list of numbers together")
@click.option("--numbers")
def add(numbers):
    command_add(numbers)

cli.add_command(greet)
cli.add_command(add)

if __name__ == '__main__':
    cli()