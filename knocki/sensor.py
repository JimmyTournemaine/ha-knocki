"""Platform for the Knocki integration sensors."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN, LOGGER
from .knocki import KnockiDevice, KnockiException


@dataclass(kw_only=True)
class KnockiSensorEntityDescription(SensorEntityDescription):  # type: ignore[misc]
    """Describes Knocki sensor entity."""

    value_fn: Callable[[KnockiDevice], StateType]


SENSOR_TYPES: tuple[KnockiSensorEntityDescription, ...] = (
    KnockiSensorEntityDescription(
        key="battery",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda device: device.battery,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Knocki sensors based on a config entry."""

    device: KnockiDevice = hass.data[DOMAIN][entry.entry_id]

    sensors = [KnockiSensorEntity(device, sensor_type) for sensor_type in SENSOR_TYPES]
    async_add_entities(sensors, True)


class KnockiSensorEntity(SensorEntity):
    """Representation of a Knocki sensor."""

    entity_description: KnockiSensorEntityDescription

    def __init__(
        self, device: KnockiDevice, entity_description: KnockiSensorEntityDescription
    ) -> None:
        """Initialize the sensor."""
        self._device = device
        self.entity_description = entity_description
        self._attr_available = False  # This overrides the default
        self._attr_unique_id = f"{device.name}_{entity_description.key}"

        LOGGER.info(self._attr_unique_id)

    def update(self) -> None:
        """Update entity state."""
        try:
            self._device.update()
        except KnockiException:
            if self.available:  # Read current state, no need to prefix with _attr_
                LOGGER.warning("Update failed for %s", self.entity_id)
            self._attr_available = False  # Set property value
            return

        self._attr_available = True
        # We don't need to check if device available here
        self._attr_native_value = self.entity_description.value_fn(
            self._device
        )  # Update "native_value" property
