# -*- coding: utf-8 -*-
"""A user model."""
import datetime as dt

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship

from ..database import Model, SurrogatePK, reference_col
from ..extensions import pwd_context


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(String(80), unique=True, nullable=False)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        """Create instance."""
        Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class User(SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(String(128), nullable=True)
    created_at = Column(DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(String(30), nullable=True)
    last_name = Column(String(30), nullable=True)
    active = Column(Boolean(), default=False)
    is_admin = Column(Boolean(), default=False)

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = pwd_context.hash(password)

    def check_password(self, value):
        """Check password."""
        return pwd_context.verify(value, self.password)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    @property
    def is_active(self):
        """Return if the user is active."""
        return self.active

    @property
    def is_authenticated(self):
        """Return if the user is authenticated."""
        return True

    @property
    def is_anonymous(self):
        """Return if the user is anonymous."""
        return False

    def get_id(self):
        """Return the user by id."""
        try:
            return self.id
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)
