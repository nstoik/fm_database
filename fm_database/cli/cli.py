import click
from .testing import commands as testing_commands
from .database import commands as database_commands


@click.group()
def entry_point():
    pass


entry_point.add_command(testing_commands.test)
entry_point.add_command(testing_commands.lint)

entry_point.add_command(database_commands.create_tables)
entry_point.add_command(database_commands.create_revision)
entry_point.add_command(database_commands.database_upgrade)
entry_point.add_command(database_commands.init)
