# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""
# pylint: disable=redefined-outer-name,invalid-name
import pytest
from _pytest.monkeypatch import MonkeyPatch
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from fm_database.base import get_base
from fm_database.settings import get_config

config = get_config(override_default="test")
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
session = sessionmaker(bind=engine)
db_session = scoped_session(session)


@pytest.fixture(scope="session")
# pylint: disable=unused-argument
def monkeysession(request):
    """Create a MonkeyPatch object that can be scoped to a session.

    https://github.com/pytest-dev/pytest/issues/363#issuecomment-289830794
    """
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest.fixture(scope="session", autouse=True)
def set_testing_env(monkeysession):
    """Set the environment variable for testing.

    This executes once for the entire session of testing.
    The environment variables are set back to the default after.
    Makes sure that the database env is also called and set.
    """
    monkeysession.setenv("FM_DATABASE_CONFIG", "test")
    yield
    monkeysession.setenv("FM_DATABASE_CONFIG", "dev")


@pytest.fixture
def dbsession():
    """Returns an sqlalchemy session."""

    yield db_session


@pytest.fixture
def tables(dbsession):
    """Create all tables for testing. Delete when done."""
    base = get_base()
    base.query = dbsession.query_property()
    base.metadata.create_all(bind=engine)
    yield
    dbsession.close()
    base.metadata.drop_all(bind=engine)
