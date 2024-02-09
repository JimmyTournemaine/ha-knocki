"""Tests for the Knocki binary sensor platform."""
import pytest

from homeassistant.const import STATE_OFF
from homeassistant.core import HomeAssistant


@pytest.mark.usefixtures("init_integration")
async def test_binary_sensors(
    hass: HomeAssistant,
) -> None:
    """Test the creation and values of the Knocki binary sensors."""
    assert (state := hass.states.get("binary_sensor.knocki_mock_title_sleep_mode"))
    assert state.state == STATE_OFF

    assert (state := hass.states.get("binary_sensor.knocki_mock_title_turbo_mode"))
    assert state.state == STATE_OFF
