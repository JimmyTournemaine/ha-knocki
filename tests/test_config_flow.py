"""Test the Knocki config flow."""
from unittest.mock import AsyncMock, patch

import pytest

from homeassistant import config_entries
from homeassistant.components.knocki.config_flow import NameAlreadyExists
from homeassistant.components.knocki.const import CONF_LOCAL_ONLY, DOMAIN
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType


async def test_form(hass: HomeAssistant, mock_setup_entry: AsyncMock) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_NAME: "My Knocki",
            CONF_LOCAL_ONLY: False,
        },
    )
    await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "My Knocki"
    assert result["data"] == {}
    assert result["options"] == {CONF_LOCAL_ONLY: False}


@pytest.mark.parametrize(
    "entry_name", ["My Knocki", "my-knocki", "my_knocki", "my knocki"]
)
async def test_form_name_already_exists(
    hass: HomeAssistant, mock_setup_entry: AsyncMock, entry_name: str
) -> None:
    """Test we handle device with same name/slug."""

    # WHEN
    with patch(
        "homeassistant.components.knocki.config_flow.ConfigFlow.validate_unique",
        side_effect=NameAlreadyExists,
    ) as mock_setup_entry:
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_NAME: entry_name,
                CONF_LOCAL_ONLY: False,
            },
        )

    # THEN
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "already_configured"}
    mock_setup_entry.assert_called_once()
