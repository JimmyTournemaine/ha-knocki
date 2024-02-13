"""Test the Knocki config flow."""
from unittest.mock import AsyncMock, patch

import pytest

from homeassistant import config_entries, data_entry_flow
from homeassistant.components.knocki.config_flow import NameAlreadyExists
from homeassistant.components.knocki.const import CONF_LOCAL_ONLY, DOMAIN
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from tests.common import MockConfigEntry # pylint: disable=no-name-in-module


async def test_init_form(hass: HomeAssistant, mock_setup_entry: AsyncMock) -> None:
    """Test we get the form and validate device creation."""
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
    ) as mock_validate_unique:
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
    mock_validate_unique.assert_called_once()


async def test_form_unexpected(
    hass: HomeAssistant,
    mock_setup_entry: AsyncMock,
) -> None:
    """Test unexpected error occurred."""

    # WHEN
    with patch(
        "homeassistant.components.knocki.config_flow.ConfigFlow.validate_unique",
        side_effect=Exception,
    ) as mock_validate_unique:
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_NAME: "Name",
                CONF_LOCAL_ONLY: False,
            },
        )

    # THEN
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "unknown"}
    mock_validate_unique.assert_called_once()


async def test_option_flow(
    hass: HomeAssistant, mock_config_entry: MockConfigEntry
) -> None:
    """Test option flow."""
    mock_config_entry.add_to_hass(hass)

    with patch("homeassistant.components.knocki.async_setup_entry", return_value=True):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()
        result = await hass.config_entries.options.async_init(
            mock_config_entry.entry_id,
            data=None,
        )

    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["step_id"] == "init"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={CONF_LOCAL_ONLY: False},
    )

    assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result["data"][CONF_LOCAL_ONLY] is False
