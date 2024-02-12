"""Constants for the Knocki integration."""

import logging

CONF_LOCAL_ONLY = "local_only"
DOMAIN = "knocki"
EVENT_TYPES = [
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
]
KNOCKI_EVENT_LISTENER = "KNOCKI_EVENT_LISTENER"
LOGGER = logging.getLogger(DOMAIN)
