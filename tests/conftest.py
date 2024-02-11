"""Common fixtures for the Knocki tests."""
from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

from freezegun.api import FrozenDateTimeFactory
import pytest

from homeassistant.components.knocki.const import CONF_LOCAL_ONLY, DOMAIN
from homeassistant.components.knocki.knocki import KnockiDevice
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry, load_json_object_fixture


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return the default mocked config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={CONF_NAME: "On Conference Table"},
        options={CONF_LOCAL_ONLY: True},
    )


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock, None, None]:
    """Mock setting up a config entry."""
    with patch(
        "homeassistant.components.knocki.async_setup_entry", return_value=True
    ) as mock_setup:
        yield mock_setup


@pytest.fixture
def device_fixture() -> str:
    """Return the device fixture for a specific device."""
    return "knc1_w"


@pytest.fixture
def mock_knocki(device_fixture: str) -> Generator[MagicMock, None, None]:
    """Return a mocked WLED client."""

    knocki = KnockiDevice(load_json_object_fixture(f"{device_fixture}.json", DOMAIN))
    knocki.title = "Mock Title"
    knocki.slug = "mock_title"
    return knocki


@pytest.fixture
async def webhook_client(hass_client) -> Generator[MagicMock, None, None]:
    """Return a client to call webhooks."""
    return await hass_client()


@pytest.fixture
async def init_integration(
    hass: HomeAssistant,
    freezer: FrozenDateTimeFactory,
    mock_config_entry: MockConfigEntry,
    mock_knocki: MagicMock,
) -> MockConfigEntry:
    """Set up the Knocki integration for testing."""
    mock_config_entry.add_to_hass(hass)

    with patch(
        "homeassistant.components.knocki.KnockiDevice.create_device",
        return_value=mock_knocki,
    ):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    # Let some time pass so coordinators can be reliably triggered by bumping
    # time by SCAN_INTERVAL
    freezer.tick(1)

    return mock_config_entry
