"""Tests for the Knocki integration."""

from homeassistant.components.knocki.const import CONF_LOCAL_ONLY, DOMAIN
from homeassistant.const import CONF_NAME

from tests.common import MockConfigEntry


async def init_integration(hass) -> MockConfigEntry:
    """Set up the Knocki integration in Home Assistant."""
    entry_data = {
        CONF_NAME: "My Knocki",
        CONF_LOCAL_ONLY: True,
    }
    entry = MockConfigEntry(domain=DOMAIN, data=entry_data, title=entry_data[CONF_NAME])
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    return entry
