"""Knocki API stub."""

from collections.abc import Callable

from homeassistant.util import slugify


class KnockiDevice:
    """Knocki device API."""

    name: str
    battery: float
    sleep_mode: bool
    turbo_mode: bool

    event_listeners: [Callable[[str], None]]

    @staticmethod
    def slug(title):
        """Slufigy the device friendly name."""
        return slugify(title)

    def __init__(self, title) -> None:
        """Set up defaults."""
        self.title = title
        self.name = self.slug(title)
        self.battery = None
        self.sleep_mode = None
        self.turbo_mode = None
        self.event_listeners = {}

    def update(self):
        """Update the device informations."""

    def knock(self, gesture: str) -> None:
        """Someone knocked."""
        for listener in self.event_listeners.values():
            listener(gesture)

    def listen(self, identifier: str, callback: Callable[[str], None]) -> None:
        """Register a listener for knock events."""
        self.event_listeners[identifier] = callback

    def remove_listener(self, identifier: str) -> Callable[[str], None]:
        """Remove a listener for knock events."""
        return self.event_listeners.pop(identifier)
