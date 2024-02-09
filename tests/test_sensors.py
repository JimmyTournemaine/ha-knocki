"""Tests for the Knocki binary sensor platform."""
import pytest

from homeassistant.components.sensor.const import SensorDeviceClass
from homeassistant.const import ATTR_DEVICE_CLASS, ATTR_UNIT_OF_MEASUREMENT, PERCENTAGE
from homeassistant.core import HomeAssistant


@pytest.mark.usefixtures("init_integration")
async def test_sensors(
    hass: HomeAssistant,
) -> None:
    """Test the creation and values of the Knocki sensors."""
    assert (state := hass.states.get("sensor.knocki_mock_title_battery"))
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == PERCENTAGE
    assert state.attributes.get(ATTR_DEVICE_CLASS) == SensorDeviceClass.BATTERY
    assert state.state == "100"
