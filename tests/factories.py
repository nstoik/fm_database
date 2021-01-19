"""Factories to help in tests."""
# pylint: disable=too-few-public-methods,no-self-argument,unused-argument
from factory import PostGenerationMethodCall, Sequence, post_generation
from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy.orm import Session

from fm_database.base import get_session
from fm_database.models.device import (
    Device,
    Grainbin,
    TemperatureCable,
    TemperatureSensor,
)
from fm_database.models.user import User

db_session = get_session()


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    @classmethod
    def create(cls, session, **kwargs):
        """Override the create method of the SQLALchemyModelFactory class.

        Adds the variable session so that the sqlalchemy_session can be
        passed in and overwritten. The sqlalchemy_session is pasased in this
        way so that the new object can be properly saved in the correct session.
        """
        cls._meta.sqlalchemy_session = session
        return super().create(**kwargs)

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = None


class UserFactory(BaseFactory):
    """User factory."""

    username = Sequence(lambda n: f"user{n}")
    email = Sequence(lambda n: f"user{n}@example.com")
    password = PostGenerationMethodCall("set_password", "example")
    active = True

    class Meta:
        """Factory configuration."""

        model = User


class DeviceFactory(BaseFactory):
    """Device factory."""

    device_id = Sequence(lambda n: f"Test Device{n}")
    hardware_version = "v1"
    software_version = "v1"

    class Meta:
        """Factory configuration."""

        model = Device


class GrainbinFactory(BaseFactory):
    """Grainbin factory."""

    device_id = "set in custom_grainbin_save"
    bus_number = Sequence(int)

    @post_generation
    def custom_grainbin_save(obj, create, extracted, **kwargs):  # noqa: N805
        """Custom function to add proper device.id to grainbin.

        I tried doing this with SubFactory, but I could not get it
        to work with also passing in a custom session object ;).
        """
        if not create:
            return
        session = Session.object_session(obj)
        device = DeviceFactory.create(session)
        device.save(session)
        obj.device_id = device.id
        return

    class Meta:
        """Factory Configuration."""

        model = Grainbin


class TemperatureCableFactory(BaseFactory):
    """TemperatureCable factory."""

    grainbin_id = "set in custom_cable_save"

    @post_generation
    def custom_cable_save(obj, create, extracted, **kwargs):  # noqa: N805
        """Custom function to add proper grainbin.id to temperaturecable.

        I tried doing this with SubFactory, but I could not get it
        to work with also passing in a custom session object ;).
        """
        if not create:
            return
        session = Session.object_session(obj)
        grainbin = GrainbinFactory.create(session)
        grainbin.save(session)
        obj.grainbin_id = grainbin.id
        return

    class Meta:
        """Factory configurations."""

        model = TemperatureCable


class TemperatureSensorFactory(BaseFactory):
    """TemperatureSensor factory."""

    cable_id = "set in custom_sensor_save"

    @post_generation
    def custom_sensor_save(obj, create, extracted, **kwargs):  # noqa: N805
        """Custom function to add proper cable.id to TemperatureSensor.

        I tried doing this with SubFactory, but I could not get it
        to work with also passing in a custom session object ;).
        """
        if not create:
            return
        session = Session.object_session(obj)
        temperature_cable = TemperatureCableFactory.create(session)
        temperature_cable.save(session)
        obj.cable_id = temperature_cable.id
        return

    class Meta:
        """Factory configurations."""

        model = TemperatureSensor
