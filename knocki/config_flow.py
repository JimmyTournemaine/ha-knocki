"""Config flow for Knocki integration."""
from __future__ import annotations

import logging
from typing import Any, Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import CONF_LOCAL_ONLY, DOMAIN
from .knocki import KnockiDevice

_LOGGER = logging.getLogger(__name__)


def get_data_schema(config_entry: Optional[config_entries.ConfigEntry] = None):
    """Get data schema for init or configure steps."""
    schema_on_init = {vol.Required(CONF_NAME): str}
    schema_on_update = {
        vol.Required(
            CONF_LOCAL_ONLY,
            default=(
                config_entry.options.get(CONF_LOCAL_ONLY)
                if config_entry is not None
                else True
            ),
        ): bool
    }

    if config_entry is None:
        return vol.Schema(schema_on_init | schema_on_update)
    return vol.Schema(schema_on_update)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Knocki."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await self.validate_input(self.hass, user_input)
            except NameAlreadyExists:
                errors["base"] = "already_configured"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=info["title"], data=info["data"], options=info["options"]
                )

        return self.async_show_form(
            step_id="user", data_schema=get_data_schema(), errors=errors
        )

    async def validate_unique(self, hass: HomeAssistant, data: dict[str, Any]) -> None:
        """Validate that name do not already exists (based on slug)."""
        slug = KnockiDevice.slug(data[CONF_NAME])
        if any(iter(slug == d.name for d in hass.data.get(DOMAIN, {}).values())):
            raise NameAlreadyExists()

    async def validate_input(
        self, hass: HomeAssistant, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Validate the user input allows us to connect."""
        await self.validate_unique(hass, data)

        return {
            "title": data[CONF_NAME],
            "data": {},
            "options": {CONF_LOCAL_ONLY: data[CONF_LOCAL_ONLY]},
        }

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return OptionsFlowHandler(config_entry)


class NameAlreadyExists(HomeAssistantError):
    """Error to indicate a device with this name already exists."""


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handler for options (reconfigure)."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=get_data_schema(self.config_entry),
        )
