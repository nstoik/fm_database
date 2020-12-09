"""Factories to help in tests."""
# pylint: disable=too-few-public-methods
from factory import PostGenerationMethodCall, SelfAttribute, Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory

from fm_database.models.device import (
    Device,
    Grainbin,
    TemperatureCable,
    TemperatureSensor,
)
from fm_database.models.user import User

from .conftest import db_session


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db_session


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

    # explicitly save the device to the database here so IDs are available to SubFactory instances.
    _ = PostGenerationMethodCall("save", db_session)

    class Meta:
        """Factory configuration."""

        model = Device


class GrainbinFactory(BaseFactory):
    """Grainbin factory."""

    device = SubFactory(DeviceFactory)
    device_id = SelfAttribute("device.id")
    bus_number = Sequence(int)

    # explicitly save the device to the database here so IDs are available to SubFactory instances.
    _ = PostGenerationMethodCall("save", db_session)

    class Meta:
        """Factory Configuration."""

        model = Grainbin
        exclude = ("device",)


class TemperatureCableFactory(BaseFactory):
    """TemperatureCable factory."""

    grainbin = SubFactory(GrainbinFactory)
    grainbin_id = SelfAttribute("grainbin.id")

    # explicitly save the device to the database here so IDs are available to SubFactory instances.
    _ = PostGenerationMethodCall("save", db_session)

    class Meta:
        """Factory configurations."""

        model = TemperatureCable
        exclude = ("grainbin",)


class TemperatureSensorFactory(BaseFactory):
    """TemperatureSensor factory."""

    temperature_cable = SubFactory(TemperatureCableFactory)
    cable_id = SelfAttribute("temperature_cable.id")

    class Meta:
        """Factory configurations."""

        model = TemperatureSensor
        exclude = "temperature_cable"
