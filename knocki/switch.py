"""Platform for the Knocki integration sensors."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.switch import (
    SwitchDeviceClass,
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, LOGGER
from .knocki import KnockiDevice


@dataclass(kw_only=True)
class KnockiSwitchEntityDescription(SwitchEntityDescription):  # type: ignore[misc]
    """Describes Knocki sensor entity."""

    value_fn: Callable[[KnockiDevice], bool | None]
    turn_on_fn: Callable[[KnockiDevice], None]
    turn_off_fn: Callable[[KnockiDevice], None]


SENSOR_TYPES: tuple[KnockiSwitchEntityDescription, ...] = (
    KnockiSwitchEntityDescription(
        key="sleep_mode",
        device_class=SwitchDeviceClass.SWITCH,
        turn_on_fn=lambda device: device.enable_sleep_mode(),
        turn_off_fn=lambda device: device.disable_sleep_mode(),
        value_fn=lambda device: device.sleep_mode,
    ),
    KnockiSwitchEntityDescription(
        key="turbo_mode",
        device_class=SwitchDeviceClass.SWITCH,
        turn_on_fn=lambda device: device.enable_turbo_mode(),
        turn_off_fn=lambda device: device.disable_turbo_mode(),
        value_fn=lambda device: device.turbo_mode,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Knocki sensors based on a config entry."""

    device: KnockiDevice = hass.data[DOMAIN][entry.entry_id]

    sensors = [KnockiSwitchEntity(device, sensor_type) for sensor_type in SENSOR_TYPES]
    async_add_entities(sensors, True)


class KnockiSwitchEntity(SwitchEntity):
    """Representation of a Knocki sensor."""

    entity_description: KnockiSwitchEntityDescription

    def __init__(
        self,
        device: KnockiDevice,
        entity_description: KnockiSwitchEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        self._device = device
        self.entity_description = entity_description
        self._attr_unique_id = f"{device.name}_{entity_description.key}"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        LOGGER.info("Turning on entity " + self.entity_description.key)
        self.entity_description.turn_on_fn(self._device)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        LOGGER.info("Turning off entity " + self.entity_description.key)
        self.entity_description.turn_off_fn(self._device)

    def update(self) -> None:
        """Update entity state."""
        self.is_on = self.entity_description.value_fn(self._device)
