"""Knocki API stub."""

from collections.abc import Callable

from homeassistant.util import slugify


class KnockiDevice:
    name: str
    battery: float
    sleep_mode: bool
    turbo_mode: bool

    event_listeners: [Callable[[str], None]]

    @staticmethod
    def slug(title):
        """Slufigy the device friendly name"""
        return slugify(title)

    def __init__(self, title):
        self.title = title
        self.name = self.slug(title)
        self.battery = None
        self.sleep_mode = None
        self.turbo_mode = None
        self.event_listeners = {}

    def update(self):
        pass

    def knock(self, gesture: str):
        for listener in self.event_listeners.values():
            listener(gesture)

    def listen(self, id: str, callback: Callable[[str], None]) -> None:
        self.event_listeners[id] = callback

    def remove_listener(self, id: str) -> Callable[[str], None]:
        return self.event_listeners.pop(id)


class KnockiException(Exception):
    pass
