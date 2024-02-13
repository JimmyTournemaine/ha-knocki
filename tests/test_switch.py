"""Tests for the Knocki switch platform."""
import pytest

from homeassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from homeassistant.const import STATE_OFF, STATE_ON
from homeassistant.core import HomeAssistant


@pytest.mark.usefixtures("init_integration")
async def test_switches(
    hass: HomeAssistant,
) -> None:
    """Test the creation and values of the Knocki switches."""
    assert (state := hass.states.get("switch.knocki_mock_title_sleep_mode"))
    assert state.state == STATE_OFF

    assert (state := hass.states.get("switch.knocki_mock_title_turbo_mode"))
    assert state.state == STATE_OFF


@pytest.mark.usefixtures("init_integration")
@pytest.mark.parametrize("switch", ["sleep_mode", "turbo_mode"])
async def test_on_off(hass: HomeAssistant, switch: str) -> None:
    """Test on/off updates."""

    entity_id = f"switch.knocki_mock_title_{switch}"

    await hass.services.async_call(
        SWITCH_DOMAIN, "turn_off", {"entity_id": entity_id}, blocking=True
    )

    state = hass.states.get(entity_id)
    assert state is not None and state.state == STATE_OFF

    await hass.services.async_call(
        SWITCH_DOMAIN, "turn_on", {"entity_id": entity_id}, blocking=True
    )

    state = hass.states.get(entity_id)
    assert state is not None and state.state == STATE_ON

    await hass.services.async_call(
        SWITCH_DOMAIN, "toggle", {"entity_id": entity_id}, blocking=True
    )

    state = hass.states.get(entity_id)
    assert state is not None and state.state == STATE_OFF
