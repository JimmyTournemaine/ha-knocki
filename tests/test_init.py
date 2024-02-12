"""Test the Knocki integration init."""
from homeassistant.components.knocki.const import DOMAIN
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry


async def test_unload_entry(
    hass: HomeAssistant, mock_config_entry: MockConfigEntry
) -> None:
    """Test successful unload of entry."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.LOADED # type: ignore[comparison-overlap]

    await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED # type: ignore[comparison-overlap]
    assert not hass.data.get(DOMAIN)
