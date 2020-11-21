# -*- coding: utf-8 -*-
"""Click commands for the database management."""
import click
from alembic import command as al_command
from alembic.config import Config as AlConfig

from fm_database.base import create_all_tables, get_session
from fm_database.models.system import SystemSetup
from fm_database.models.user import User
from fm_database.settings import get_config


# pylint: disable=unused-import,import-outside-toplevel
@click.command()
def create_tables():
    """Create database tables."""

    click.echo("create database")
    from fm_database.models.device import Device  # noqa: F401

    click.echo("creating all tables")
    create_all_tables()

    config = get_config()
    alembic_cnf = AlConfig(config.PROJECT_ROOT + "/migrations/alembic.ini")
    alembic_cnf.set_main_option("script_location", config.PROJECT_ROOT + "/migrations")
    click.echo("stamping alembic head")
    al_command.stamp(alembic_cnf, "head")
    click.echo("done")


@click.command()
def init():
    """Init database. Create a new user named admin with password admin."""

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


@click.command()
@click.option(
    "--message",
    prompt="Provide a message for the revision",
    help="Message for revision",
)
def create_revision(message):
    """Create a database migration using alembic."""

    config = get_config()
    alembic_cnf = AlConfig(config.PROJECT_ROOT + "/migrations/alembic.ini")
    alembic_cnf.set_main_option("script_location", config.PROJECT_ROOT + "/migrations")

    al_command.revision(alembic_cnf, message=message, autogenerate=True)


@click.command()
@click.option(
    "--revision",
    default="head",
    prompt="What revision to upgrade to?",
    help="What revision to upgrade to",
)
def database_upgrade(revision):
    """Upgrade database to given revision."""

    config = get_config()
    alembic_cnf = AlConfig(config.PROJECT_ROOT + "/migrations/alembic.ini")
    alembic_cnf.set_main_option("script_location", config.PROJECT_ROOT + "/migrations")

    al_command.upgrade(alembic_cnf, revision)
