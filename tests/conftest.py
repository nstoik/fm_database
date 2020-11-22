# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""
# pylint: disable=redefined-outer-name,invalid-name
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from fm_database.base import get_base
from fm_database.settings import get_config

config = get_config(override_default="test")
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
session = sessionmaker(bind=engine)
db_session = scoped_session(session)


@pytest.fixture
def dbsession():
    """Returns an sqlalchemy session."""

    yield db_session


@pytest.fixture
def tables(dbsession):
    """Create all tables for testing. Delete when done."""
    base = get_base(with_query=True)
    base.query = dbsession.query_property()
    base.metadata.create_all(bind=engine)
    yield
    dbsession.close()
    base.metadata.drop_all(bind=engine)
