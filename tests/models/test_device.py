"""Test device models."""
import datetime as dt

import pytest

from fm_database.models.device import (
    Device,
    Grainbin,
    TemperatureCable,
    TemperatureSensor,
)

from ..factories import (
    DeviceFactory,
    GrainbinFactory,
    TemperatureCableFactory,
    TemperatureSensorFactory,
)


@pytest.mark.usefixtures("tables")
class TestTemperatureSensor:
    """Temperature Sensor model tests."""

    @staticmethod
    def test_create_temperature_sensor(dbsession):
        """Create a temperature sensor instance."""
        temperature_cable = TemperatureCableFactory()
        temperature_cable.save(dbsession)

        temperature_sensor = TemperatureSensor(temperature_cable.id)
        temperature_sensor.save(dbsession)

        assert temperature_sensor.cable_id == temperature_cable.id
        assert temperature_sensor.last_value == "unknown"

    @staticmethod
    def test_get_temperature_sensor_by_id(dbsession):
        """Test retrieving a temperature sensor by its id."""
        temperature_cable = TemperatureCableFactory()
        temperature_cable.save(dbsession)

        temperature_sensor = TemperatureSensor(temperature_cable.id)
        temperature_sensor.save(dbsession)

        retrieved = TemperatureSensor.get_by_id(temperature_sensor.id)
        assert retrieved == temperature_sensor

    @staticmethod
    def test_temperature_sensor_factory(dbsession):
        """Test the TemperatureSensor factory."""
        temperature_sensor = TemperatureSensorFactory()
        temperature_sensor.save(dbsession)

        retrieved = TemperatureSensor.get_by_id(temperature_sensor.id)
        assert retrieved == temperature_sensor

    @staticmethod
    def test_temperature_sensor_properties(dbsession):
        """Test TemperatureSensor properties."""
        temperature_sensor = TemperatureSensorFactory()
        temperature_sensor.save(dbsession)

        assert temperature_sensor.templow is None
        assert temperature_sensor.temphigh is None
        assert temperature_sensor.last_value == "unknown"
        assert isinstance(temperature_sensor.cable_id, int)

    @staticmethod
    def test_multiple_temperature_sensors_per_cable(dbsession):
        """Test adding multiple temperature sensors to the same cable."""
        temperature_cable = TemperatureCableFactory()
        temperature_cable.save(dbsession)

        for _ in range(5):
            sensor = TemperatureSensor(temperature_cable.id)
            sensor.save(dbsession)

        assert isinstance(temperature_cable.sensors, list)
        assert len(temperature_cable.sensors) == 5


@pytest.mark.usefixtures("tables")
class TestTemperatureCable:
    """Temperature Cable model tests."""

    @staticmethod
    def test_create_temperature_cable(dbsession):
        """Create a temperature cable instance."""
        grainbin = GrainbinFactory()
        grainbin.save(dbsession)

        temperature_cable = TemperatureCable(grainbin.id)
        temperature_cable.save(dbsession)

        assert temperature_cable.grainbin_id == grainbin.id

    @staticmethod
    def test_get_temperature_cable_by_id(dbsession):
        """Test retrieving a temperature cable by its id."""
        grainbin = GrainbinFactory()
        grainbin.save(dbsession)

        temperature_cable = TemperatureCable(grainbin.id)
        temperature_cable.save(dbsession)

        retrieved = TemperatureCable.get_by_id(temperature_cable.id)
        assert retrieved == temperature_cable

    @staticmethod
    def test_temperature_cable_factory(dbsession):
        """Test the TemperatureCable factory."""
        temperature_cable = TemperatureCableFactory()
        temperature_cable.save(dbsession)

        retrieved = TemperatureCable.get_by_id(temperature_cable.id)
        assert retrieved == temperature_cable

    @staticmethod
    def test_temperature_cable_properties(dbsession):
        """Test TemperatureCable properties."""
        temperature_cable = TemperatureCableFactory()
        temperature_cable.save(dbsession)

        assert temperature_cable.sensor_count == 0
        assert temperature_cable.cable_type == "temperature"
        assert temperature_cable.bin_cable_number == 0
        assert isinstance(temperature_cable.grainbin_id, int)

    @staticmethod
    def test_multiple_temperature_cables_per_bin(dbsession):
        """Test adding multiple temperature cables to the same grainbin."""
        grainbin = GrainbinFactory()
        grainbin.save(dbsession)

        for _ in range(5):
            cable = TemperatureCable(grainbin.id)
            cable.save(dbsession)

        assert isinstance(grainbin.cables, list)
        assert len(grainbin.cables) == 5


@pytest.mark.usefixtures("tables")
class TestGrainbin:
    """Grainbin model tests."""

    @staticmethod
    def test_create_grainbin(dbsession):
        """Create a grainbin instance."""
        device = DeviceFactory()
        device.save(dbsession)
        grainbin = Grainbin(device_id=device.id, bus_number=1)
        grainbin.save(dbsession)

        assert grainbin.device_id == device.id
        assert grainbin.bus_number == 1

    @staticmethod
    def test_get_grainbin_by_id(dbsession):
        """Test retrieving a grainbin by its ID."""
        device = DeviceFactory()
        device.save(dbsession)
        grainbin = Grainbin(device_id=device.device_id, bus_number=1)
        grainbin.save(dbsession)

        retrieved = Grainbin.get_by_id(grainbin.id)

        assert grainbin == retrieved

    @staticmethod
    def test_grainbin_factory(dbsession):
        """Test GrainbinFactory."""

        grainbin = GrainbinFactory()
        grainbin.save(dbsession)

        retrieved = Grainbin.get_by_id(grainbin.id)

        assert grainbin == retrieved

    @staticmethod
    def test_grainbin_properties(dbsession):
        """Test all Grainbin properties."""
        grainbin = GrainbinFactory()
        grainbin.save(dbsession)

        assert isinstance(grainbin.creation_time, dt.datetime)
        assert isinstance(grainbin.last_updated, dt.datetime)
        assert grainbin.name == "New"
        assert grainbin.grainbin_type == "standard"
        assert grainbin.sensor_type == "temperature"
        assert grainbin.location == "Not Set"
        assert grainbin.description == "Not Set"
        assert isinstance(grainbin.total_updates, int)
        assert grainbin.average_temp is None
        assert isinstance(grainbin.bus_number, int)
        assert not grainbin.user_configured


@pytest.mark.usefixtures("tables")
class TestDevice:
    """Device model tests."""

    @staticmethod
    def test_create_device(dbsession):
        """Create a device instance."""

        device = Device(
            device_id="Test Device", hardware_version="1", software_version="1"
        )
        device.save(dbsession)

        assert device.device_id == "Test Device"
        assert device.hardware_version == "1"
        assert device.software_version == "1"

    @staticmethod
    def test_get_device_by_id(dbsession):
        """Test retrieving a device by its ID."""

        device = Device(
            device_id="Test Device", hardware_version="1", software_version="1"
        )
        device.save(dbsession)

        retrieved = Device.get_by_id(device.id)

        assert device == retrieved

    @staticmethod
    def test_device_factory(dbsession):
        """Test DeviceFactory."""

        device = DeviceFactory()
        device.save(dbsession)

        retrieved = Device.get_by_id(device.id)

        assert device == retrieved

    @staticmethod
    def test_device_properties(dbsession):
        """Test all Device properties."""

        device = DeviceFactory()
        device.save(dbsession)

        assert isinstance(device.creation_time, dt.datetime)
        assert isinstance(device.last_updated, dt.datetime)
        assert device.name == "not set"
        assert device.location == "not set"
        assert device.description == "not set"
        assert not bool(device.connected)
        assert not bool(device.user_configured)
        assert device.last_update_received is None
        assert device.interior_temp is None
        assert device.exterior_temp is None
        assert device.device_temp is None
        assert device.uptime is None
        assert device.current_time is None
        assert device.load_avg is None
        assert device.disk_total is None
        assert device.disk_used is None
        assert device.disk_free is None
