import click

from alembic import command as al_command
from alembic.config import Config as AlConfig

from fm_database.settings import get_config
from fm_database.models.system import SystemSetup
from fm_database.models.user import User
from fm_database.base import get_session, create_all_tables


@click.group()
def cli():
    """Main entry point"""


@cli.command("create_tables")
def create_tables():
    """create database tables
    """
    click.echo("create database")
    from fm_database.models.device import Device
    click.echo("creating all tables")
    create_all_tables()

    config = get_config()
    alembic_cnf = AlConfig(config.APP_DIR + '/alembic.ini')
    alembic_cnf.set_main_option('script_location', config.APP_DIR + '/alembic')
    click.echo("stamping alembic head")
    al_command.stamp(alembic_cnf, 'head')
    click.echo("done")


@cli.command("init")
def init():
    """Init database. Create a new user named admin 
    with password admin
    """
    click.echo("creating user")
    user = User(
        username='admin',
        email='admin@mail.com',
        password='admin',
        active=True,
        is_admin=True
    )
    session = get_session()
    session.add(user)
    click.echo("created user admin")

    click.echo("inserting SystemSetup record")
    system_setup = SystemSetup()
    session.add(system_setup)
    session.commit()



@cli.command("create_revision")
@click.option('--message', prompt='Provide a message for the revision', help='Message for revision')
def create_revision(message):
    """
    create a database migration using alembic
    """

    config = get_config()
    alembic_cnf = AlConfig(config.APP_DIR + '/alembic.ini')
    alembic_cnf.set_main_option('script_location', config.APP_DIR + '/alembic')

    al_command.revision(alembic_cnf, message=message, autogenerate=True)


@cli.command("database_upgrade")
@click.option('--revision', default='head', prompt='What revision to upgrade to?', help='What revision to upgrade to')
def database_upgrade(revision):
    """
    upgrade database to given revision
    """

    config = get_config()
    alembic_cnf = AlConfig(config.APP_DIR + '/alembic.ini')
    alembic_cnf.set_main_option('script_location', config.APP_DIR + '/alembic')

    al_command.upgrade(alembic_cnf, revision)


if __name__ == "__main__":
    cli()
