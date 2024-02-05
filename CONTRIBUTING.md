# Contributing to the Knocki integration

Everybody is invited and welcome to contribute.

The process is similar to what is requested for [Home Assistant contributions](https://github.com/home-assistant/core/blob/dev/CONTRIBUTING.md).

Still interested? Then you should take a peek at the [developer documentation](https://developers.home-assistant.io/) to get more details, about how Home Assistant development works and create your development workspace.

Then, from your development container:

- Clone your knocki integration fork into /workspaces/ha-knocki
- Create links to integrate knocki integration sources into home assistant components.

```bash
git clone git@<your-fork> /workspaces/ha-knocki
ln -s /workspaces/ha-knocki/src /workspaces/ha-core/homeassistant/components/knocki
ln -s /workspaces/ha-knocki/tests /workspaces/ha-core/tests/components/knocki
ln -s /workspaces/ha-knocki/blueprints/automation/ /workspaces/ha-core/config/blueprints/automation/knocki
```

To simplify your code navigation, you can "Add folder to workspace" and select `/workspaces/ha-knocki` (VS Code window may reload).

## Feature suggestions

If you want to suggest a new feature for Home Assistant (e.g., new integrations), please open an issue in the [Github issue tracker](https://github.com/JimmyTournemaine/ha-knocki/issues).
