# Knocki integration for Home Assistant

![stability-wip](https://img.shields.io/badge/stability-wip-orange.svg)
![issues](https://img.shields.io/github/issues/JimmyTournemaine/ha-knocki)
![license](https://img.shields.io/github/license/JimmyTournemaine/ha-knocki)
![gitmoji](https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=flat-square)

[Knocki](http://knocki.com/) is a small wireless smart device that transforms ordinary surfaces into touch controls.
The Knocki developer do not provider any Open API yet.

Therefore, this repository is a first step of what could be developed in the future.

## Installation

Get the latest release and deploy it to your `custom_components` folder.
Restart HA.

## Configuration

## Implementation

As introduced above, there is no usable API at the moment. Thus, some sensors are only stubs for the moment but allow us to prepare for the future.

### Integration sensors

- sensor.battery: (stub) always unknown for now.
- binary_sensor.sleep_mode: (stub) always unknown for now.
- binary_sensor.turbo_mode: (stub) always unknown for now.
- event.knock: When you knocked, the (well configured) knocki would trigger this event.
