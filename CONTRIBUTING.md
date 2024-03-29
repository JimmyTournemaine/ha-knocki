# Contributing to the Knocki integration

Everybody is invited and welcome to contribute.

The process is similar to what is requested for [Home Assistant contributions](https://github.com/home-assistant/core/blob/dev/CONTRIBUTING.md).

Still interested? Then you should take a peek at the [developer documentation](https://developers.home-assistant.io/) to get more details, about how Home Assistant development works and create your development workspace.

## Local development

Then, from your development container:

- Clone your knocki integration fork into /workspaces/ha-knocki
- Create links to integrate knocki integration sources into home assistant components.

```bash
git clone git@<your-fork> /workspaces/ha-knocki
ln -s /workspaces/ha-knocki/knocki /workspaces/ha-core/homeassistant/components/knocki
ln -s /workspaces/ha-knocki/tests /workspaces/ha-core/tests/components/knocki
ln -s /workspaces/ha-knocki/blueprints/automation/ /workspaces/ha-core/config/blueprints/automation/knocki
```
Those links are used to develop the integration with the same level of standards as Home Assistant internal integrations.

### Pre-Commit Hooks

Before any commit or push, run the following from `/workspaces/ha-knocki`:

```bash
pre-commit run --files $(find -L ./homeassistant/components/knocki ./tests/components/knocki)
```

### Check unit tests

You should check that no unit test is failing and check your code coverage.
Because of the symlinks, you should run the following to benefit from VSCode plugins.

```bash
pytest tests/components/knocki --doctest-modules --cov=./homeassistant/components/knocki --cov-report=xml --cov-report=term; sed -i 's|<source>/workspaces/ha-knocki/knocki|<source>/workspaces/ha-core/homeassistant/components/knocki|g' coverage.xml
```

## Feature suggestions

If you want to suggest a new feature for Home Assistant (e.g., new integrations), please open an issue in the [Github issue tracker](https://github.com/JimmyTournemaine/ha-knocki/issues).
