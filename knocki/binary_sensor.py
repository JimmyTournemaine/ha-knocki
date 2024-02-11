"""Platform for the Knocki integration sensors."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, LOGGER
from .knocki import KnockiDevice, KnockiException


@dataclass(kw_only=True)
class KnockiBinarySensorEntityDescription(BinarySensorEntityDescription):  # type: ignore[misc]
    """Describes Knocki sensor entity."""

    value_fn: Callable[[KnockiDevice], bool | None]


SENSOR_TYPES: tuple[KnockiBinarySensorEntityDescription, ...] = (
    KnockiBinarySensorEntityDescription(
        key="sleep_mode",
        value_fn=lambda device: device.sleep_mode,
    ),
    KnockiBinarySensorEntityDescription(
        key="turbo_mode",
        value_fn=lambda device: device.turbo_mode,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Knocki sensors based on a config entry."""

    device: KnockiDevice = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        KnockiBinarySensorEntity(device, sensor_type) for sensor_type in SENSOR_TYPES
    ]
    async_add_entities(sensors, True)


class KnockiBinarySensorEntity(BinarySensorEntity):
    """Representation of a Knocki sensor."""

    entity_description: KnockiBinarySensorEntityDescription

    def __init__(
        self,
        device: KnockiDevice,
        entity_description: KnockiBinarySensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        self._device = device
        self.entity_description = entity_description
        self._attr_available = False  # This overrides the default
        self._attr_unique_id = f"{device.name}_{entity_description.key}"

    def update(self) -> None:
        """Update entity state."""
        try:
            self._device.update()
        except KnockiException:
            if self.available:
                LOGGER.warning("Update failed for %s", self.entity_id)
            self._attr_available = False
            return

        self._attr_available = True
        # We don't need to check if device available here
        self.is_on = self.entity_description.value_fn(
            self._device
        )  # Update "native_value" property
