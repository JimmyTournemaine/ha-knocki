"""Tests for the Knocki binary sensor platform."""
import pytest
from homeassistant.components.knocki.const import LOGGER

from homeassistant.components.sensor.const import SensorDeviceClass
from homeassistant.const import ATTR_DEVICE_CLASS, ATTR_UNIT_OF_MEASUREMENT, PERCENTAGE
from homeassistant.core import HomeAssistant
from freezegun.api import FrozenDateTimeFactory


@pytest.mark.usefixtures("init_integration")
async def test_events(
    hass: HomeAssistant,
) -> None:
    """Test the creation and values of the Knocki events."""
    assert (state := hass.states.get("event.knocki_mock_title_knock"))
    assert state.state == "unknown"


@pytest.mark.usefixtures("init_integration")
async def test_events_update(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, mock_knocki
) -> None:
    """Test state update of the Knocki event."""
    assert (state := hass.states.get("event.knocki_mock_title_knock"))
    assert state.state == "unknown"

    mock_knocki.knock("3taps")
    await hass.async_block_till_done()

    assert (state := hass.states.get("event.knocki_mock_title_knock"))
    assert state.state != "unknown"
    assert state.attributes.get("event_type") == "3taps"
