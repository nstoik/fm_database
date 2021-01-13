# -*- coding: utf-8 -*-
"""Click commands for the database management."""
import click
from alembic import command as al_command
from alembic.config import Config as AlConfig

from fm_database.base import create_all_tables, drop_all_tables, get_base, get_session

# import all models so they are available to the SqlAlchemy base
from fm_database.models.device import (  # noqa: F401  pylint: disable=unused-import
    Device,
)
from fm_database.models.message import (  # noqa: F401  pylint: disable=unused-import
    Message,
)
from fm_database.models.system import SystemSetup
from fm_database.models.user import User
from fm_database.settings import get_config


@click.group()
def create():
    """Command group for database create commands."""


@create.command()
@click.option(
    "--confirm",
    default=False,
    is_flag=True,
    help="Confirm this action. This will delete all previous database data.",
)
def delete_all_data(confirm):
    """Delete all data from the database."""

    if not confirm:
        click.echo("Action was not confirmed. No change made.")
    else:
        click.echo("deleting all data from the database.")

        base = get_base()
        session = get_session()
        for table in reversed(base.meta.sorted_tables):
            session.execute(table.delete())
        session.commit()

        click.echo("done")


@create.command()
@click.pass_context
def recreate_database(ctx):
    """Drop and recreate database tables."""

    click.echo("dropping all tables")
    drop_all_tables()
    ctx.forward(create_tables)


@create.command()
def create_tables():
    """Create database tables."""

    click.echo("creating all tables")
    create_all_tables()

    config = get_config()
    alembic_cnf = AlConfig(config.PROJECT_ROOT + "/migrations/alembic.ini")
    alembic_cnf.set_main_option("script_location", config.PROJECT_ROOT + "/migrations")
    click.echo("stamping alembic head")
    al_command.stamp(alembic_cnf, "head")
    click.echo("done")


@create.command()
def initialize_database():
    """initialize database for first time. Create a new user named admin with password admin."""

    click.echo("creating user")
    user = User(
        username="admin",
        email="admin@mail.com",
        password="admin",
        active=True,
        is_admin=True,
    )
    session = get_session()
    session.add(user)
    click.echo("created user admin")

    click.echo("inserting SystemSetup record")
    system_setup = SystemSetup()
    session.add(system_setup)
    session.commit()
