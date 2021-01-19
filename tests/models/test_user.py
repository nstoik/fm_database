"""Test user models."""
import datetime as dt

import pytest

from fm_database.models.user import Role, User

from ..factories import UserFactory


@pytest.mark.usefixtures("tables")
class TestUser:
    """User tests."""

    @staticmethod
    def test_get_by_id(dbsession):
        """Get user by ID."""
        user = User("foo", "foo@bar.com")
        user.save(dbsession)

        retrieved = User.get_by_id(user.id)
        assert retrieved.id == user.id

    @staticmethod
    def test_created_at_defaults_to_datetime(dbsession):
        """Test creation date."""
        user = User(username="foo", email="foo@bar.com")
        user.save(dbsession)
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    @staticmethod
    def test_password_is_nullable(dbsession):
        """Test null password."""
        user = User(username="foo", email="foo@bar.com")
        user.save(dbsession)
        assert user.password is None

    @staticmethod
    def test_factory(dbsession):
        """Test user factory."""
        user = UserFactory.create(dbsession, password="myprecious")
        dbsession.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.is_admin is False
        assert user.active is True
        assert user.check_password("myprecious")

    @staticmethod
    def test_check_password(dbsession):
        """Check password."""
        user = User.create(
            dbsession, username="foo", email="foo@bar.com", password="foobarbaz123"
        )
        assert user.check_password("foobarbaz123") is True
        assert user.check_password("barfoobaz") is False

    @staticmethod
    def test_full_name(dbsession):
        """User full name."""
        user = UserFactory.create(dbsession, first_name="Foo", last_name="Bar")
        assert user.full_name == "Foo Bar"

    @staticmethod
    def test_roles(dbsession):
        """Add a role to a user."""
        role = Role(name="admin")
        role.save(dbsession)
        user = UserFactory.create(dbsession)
        user.roles.append(role)
        user.save(dbsession)
        assert role in user.roles

    @staticmethod
    def test_multiple_roles(dbsession):
        """Add multiple roles and users."""
        role1 = Role(name="admin")
        role1.save(dbsession)
        role2 = Role(name="test")
        role2.save(dbsession)
        user1 = UserFactory.create(dbsession)
        user1.roles.append(role1)
        user1.roles.append(role2)
        user1.save(dbsession)
        user2 = UserFactory.create(dbsession)
        user2.roles.append(role1)
        user2.save(dbsession)
        assert role1 in user1.roles
        assert role2 in user1.roles
        assert role1 in user2.roles
        assert user1 in role1.users
        assert user2 in role1.users
