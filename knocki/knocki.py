"""Knocki API stub."""

from collections.abc import Callable

from homeassistant.util import slugify

from .const import LOGGER


class KnockiDevice:
    """Knocki device API."""

    DEFAULT_VALUES = {
        "battery": 100,
        "sleep_mode": False,
        "turbo_mode": False,
    }
    name: str
    battery: float
    sleep_mode: bool
    turbo_mode: bool
    event_listeners: dict[str, Callable[[str], None]]

    @staticmethod
    def create_device(dictionary):
        """Create a new knocki device."""
        return KnockiDevice(dictionary)

    @staticmethod
    def slug(title):
        """Slufigy the device friendly name."""
        return slugify(title)

    def __init__(self, dictionary) -> None:
        """Set up defaults."""
        self.event_listeners = {}

        for k, v in {**self.DEFAULT_VALUES, **dictionary}.items():
            setattr(self, k, v)

    @property
    def title(self):
        """The title property."""
        return self._title

    @title.setter
    def title(self, value):
        """Title setter."""
        self._title = value
        self.name = self.slug(value)

    def update(self):
        """Update the device information."""

    def knock(self, gesture: str) -> None:
        """Someone knocked."""
        LOGGER.info("Someone knock")
        for listener in self.event_listeners.values():
            listener(gesture)

    def listen(self, identifier: str, callback: Callable[[str], None]) -> None:
        """Register a listener for knock events."""
        self.event_listeners[identifier] = callback

    def remove_listener(self, identifier: str) -> Callable[[str], None]:
        """Remove a listener for knock events."""
        return self.event_listeners.pop(identifier)

    def enable_sleep_mode(self) -> None:
        """Enable sleep mode."""
        self.sleep_mode = True

    def disable_sleep_mode(self) -> None:
        """Disable sleep mode."""
        self.sleep_mode = False

    def enable_turbo_mode(self) -> None:
        """Enable turbo mode."""
        self.turbo_mode = True

    def disable_turbo_mode(self) -> None:
        """Disable turbo mode."""
        self.turbo_mode = False


class KnockiException(Exception):
    """Generic exception with Knocki API."""
