"""Tests for the Knocki binary sensor platform."""
from http import HTTPStatus
from unittest.mock import patch

import pytest

from homeassistant.components.knocki.const import EVENT_TYPES


@pytest.mark.usefixtures("init_integration")
@pytest.mark.parametrize("gesture", iter(EVENT_TYPES))
async def test_webhook_trigger_knock(webhook_client, mock_knocki, gesture) -> None:
    """Test that webhook fire events."""

    webhook_id = mock_knocki.name

    with patch.object(mock_knocki, "knock") as event_mock:
        resp = await webhook_client.post(
            f"/api/webhook/{webhook_id}",
            json={"gesture": gesture},
        )

    assert resp.status == HTTPStatus.OK
    event_mock.assert_called_with(gesture)


@pytest.mark.usefixtures("init_integration")
@pytest.mark.parametrize("gesture", ["8taps"])
async def test_webhook_invalid_gesture(webhook_client, mock_knocki, gesture) -> None:
    """Test that webhook fire events."""

    webhook_id = mock_knocki.name

    with patch.object(mock_knocki, "knock") as event_mock:
        resp = await webhook_client.post(
            f"/api/webhook/{webhook_id}",
            json={"gesture": gesture},
        )

    assert resp.status == HTTPStatus.BAD_REQUEST
    event_mock.assert_not_called()


@pytest.mark.usefixtures("init_integration")
async def test_webhook_missing_gesture(webhook_client, mock_knocki) -> None:
    """Test that webhook fire events."""

    webhook_id = mock_knocki.name

    with patch.object(mock_knocki, "knock") as event_mock:
        resp = await webhook_client.post(
            f"/api/webhook/{webhook_id}",
            json={"key": "value"},
        )

    assert resp.status == HTTPStatus.BAD_REQUEST
    event_mock.assert_not_called()
