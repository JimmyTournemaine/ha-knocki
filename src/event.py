"""Platform for the Knocki integration sensors."""
from __future__ import annotations
import asyncio
from datetime import datetime

from homeassistant.components.event import (
    EventDeviceClass,
    EventEntity,
    EventEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, KNOCKI_EVENT_LISTENER, LOGGER
from .knocki import KnockiDevice

SENSOR_TYPES: tuple[EventEntityDescription, ...] = (
    EventEntityDescription(
        key="knock",
        device_class=EventDeviceClass.BUTTON,
        event_types=[
            "3taps",
            "4taps",
            "5taps",
            "6taps",
            "2taps_2taps",
            "2taps_4taps",
            "2taps_5taps",
            "2taps_3taps_2taps",
            "2taps_3taps_3taps",
            "2taps_3taps_4taps",
        ],
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Knocki sensors based on a config entry."""

    device: KnockiDevice = hass.data[DOMAIN][entry.entry_id]

    sensors = [KnockEventEntity(device, sensor_type) for sensor_type in SENSOR_TYPES]
    async_add_entities(sensors, True)


class KnockEventEntity(EventEntity):
    def __init__(
        self,
        device: KnockiDevice,
        entity_description: EventEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        self._device = device
        self.entity_description = entity_description
        # self._attr_available = False  # This overrides the default
        self._attr_unique_id = f"{device.name}_{entity_description.key}"

    @callback
    def _async_handle_event(self, event: str) -> None:
        """Handle knock event."""
        LOGGER.info("Triggered event: %s", event)
        self._trigger_event(event)
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Register callbacks with your device API/library."""
        self._device.listen(KNOCKI_EVENT_LISTENER, self._async_handle_event)
