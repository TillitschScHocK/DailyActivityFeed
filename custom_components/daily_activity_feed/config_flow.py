"""Config flow for Daily Activity Feed integration."""
import logging
import aiohttp
import async_timeout
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    DOMAIN,
    CONF_ADDON_URL,
    CONF_SCAN_INTERVAL,
    DEFAULT_ADDON_URL,
    DEFAULT_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class DailyActivityFeedConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Daily Activity Feed."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate the addon URL
            addon_url = user_input[CONF_ADDON_URL]
            
            if await self._test_connection(addon_url):
                # Create entry
                return self.async_create_entry(
                    title="Daily Activity Feed",
                    data=user_input,
                )
            else:
                errors["base"] = "cannot_connect"

        # Show form
        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_ADDON_URL, default=DEFAULT_ADDON_URL
                ): str,
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=300)),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def _test_connection(self, addon_url: str) -> bool:
        """Test if we can connect to the addon."""
        try:
            session = async_get_clientsession(self.hass)
            async with async_timeout.timeout(10):
                async with session.get(f"{addon_url}/") as response:
                    return response.status == 200
        except Exception as err:
            _LOGGER.error("Error testing connection: %s", err)
            return False

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return DailyActivityFeedOptionsFlow(config_entry)


class DailyActivityFeedOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Daily Activity Feed."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_ADDON_URL,
                        default=self.config_entry.data.get(
                            CONF_ADDON_URL, DEFAULT_ADDON_URL
                        ),
                    ): str,
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.data.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=10, max=300)),
                }
            ),
        )
