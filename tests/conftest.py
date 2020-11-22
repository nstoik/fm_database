# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""
# pylint: disable=redefined-outer-name
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from fm_database.base import get_base
from fm_database.settings import get_config


@pytest.fixture
def engine():
    """Return the sqlalchemy engine for testing."""

    config = get_config(override_default="test")
    return create_engine(config.SQLALCHEMY_DATABASE_URI)


@pytest.fixture
def tables(engine):
    """Create all tables for testing. Delete when done."""
    base = get_base(with_query=True)
    base.metadata.create_all(bind=engine)
    yield
    base.metadata.drop_all(bind=engine)


@pytest.fixture
def dbsession(engine):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    session = sessionmaker(bind=engine)
    db_session = scoped_session(session)

    yield db_session
