"""The Knocki integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, KNOCKI_EVENT_LISTENER
from .knocki import KnockiDevice
from .webhook import KnockiWebhookHandler

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.SWITCH, Platform.EVENT]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Knocki from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    # 1. Create API instance
    device = KnockiDevice.create_device({"title": entry.title})

    # 2. Validate the API connection (and authentication)
    # Nothing yet

    # 3. Store an API object for your platforms to access
    hass.data[DOMAIN][entry.entry_id] = device

    # Register platforms entities
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register webhook
    webhook = KnockiWebhookHandler.get_webhook(device.name)
    await webhook.async_register(hass, entry)

    # Register update listeners
    entry.async_on_unload(entry.add_update_listener(webhook.config_update_listener))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        # Pop entry from domain
        device: KnockiDevice = hass.data[DOMAIN].pop(entry.entry_id)

        # Cleanup listener
        device.remove_listener(KNOCKI_EVENT_LISTENER)

        # Cleanup webhook
        webhook = KnockiWebhookHandler.get_webhook(device.name)
        await webhook.async_unregister(hass)

    return unload_ok
