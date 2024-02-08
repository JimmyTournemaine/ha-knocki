"""Platform for the Knocki integration webhook."""

from http.client import HTTPException

from aiohttp import web

from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .const import CONF_LOCAL_ONLY, DOMAIN, LOGGER
from .knocki import KnockiDevice

HTTP_OK = 200
HTTP_BAD_REQUEST = 400


class KnockiWebhook:
    """Self-registration and handle a webhook callback."""

    webhook_id: str
    allowed_methods = ["POST"]

    def __init__(self, webhook_id) -> None:
        """Init a webhook."""
        self.webhook_id = webhook_id

    async def async_register(
        self, hass: HomeAssistant, entry: config_entries.ConfigEntry
    ):
        """Register the webhook."""
        hass.components.webhook.async_register(
            DOMAIN,
            f"Knocki Webhook for {entry.title}",
            self.webhook_id,
            self.async_handle_webhook,
            local_only=entry.options[CONF_LOCAL_ONLY],
            allowed_methods=self.allowed_methods,
        )

    async def async_unregister(self, hass: HomeAssistant):
        """Unregister the webhook."""
        hass.components.webhook.async_unregister(self.webhook_id)

    async def async_handle_webhook(
        self, hass: HomeAssistant, webhook_id: str, request: web.Request
    ) -> web.Response:
        """Handle webhook callback."""
        try:
            payload = await request.json()

            device: KnockiDevice = next(
                iter(
                    [
                        device
                        for device in hass.data[DOMAIN].values()
                        if device.name == webhook_id
                    ]
                )
            )

            device.knock(payload["gesture"])

        except HTTPException as ex:
            LOGGER.error("Error processing webhook payload: %s", ex)
            return web.Response(status=HTTP_BAD_REQUEST)

        return web.Response(text="Webhook received", status=HTTP_OK)

    async def config_update_listener(
        self, hass: HomeAssistant, entry: config_entries.ConfigEntry
    ):
        """Handle options update. Re-register the webhook."""
        await self.async_unregister(hass)
        await self.async_register(hass, entry)


class KnockiWebhookHandler:
    """Handler for KnockiWebhook instances."""

    webhooks = {}

    @staticmethod
    def get_webhook(webhook_id) -> KnockiWebhook:
        """Get a KnockiWebhook by identifier or create one if unknown."""
        if webhook_id in KnockiWebhookHandler.webhooks:
            webhook = KnockiWebhookHandler.webhooks[webhook_id]
        else:
            webhook = KnockiWebhook(webhook_id)
            KnockiWebhookHandler.webhooks[webhook_id] = webhook

        return webhook
