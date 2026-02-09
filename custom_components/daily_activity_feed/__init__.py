"""Daily Activity Feed Integration"""
import logging
from datetime import datetime
from typing import Any

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.const import Platform
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    DOMAIN,
    CONF_ADDON_URL,
    SERVICE_ADD_EVENT,
    ATTR_TYPE,
    ATTR_TITLE,
    ATTR_TEXT,
    ATTR_IMAGE,
    ATTR_CAMERA_ENTITY,
    ATTR_TIMESTAMP,
    ATTR_PRIORITY,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]

# Service Schema
SERVICE_ADD_EVENT_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_TYPE): cv.string,
        vol.Required(ATTR_TITLE): cv.string,
        vol.Required(ATTR_TEXT): cv.string,
        vol.Optional(ATTR_IMAGE): cv.string,
        vol.Optional(ATTR_CAMERA_ENTITY): cv.entity_id,
        vol.Optional(ATTR_TIMESTAMP): cv.string,
        vol.Optional(ATTR_PRIORITY, default="normal"): vol.In(["low", "normal", "high"]),
    }
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Daily Activity Feed from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Register update listener
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    
    # Register services (only once)
    if not hass.services.has_service(DOMAIN, SERVICE_ADD_EVENT):
        await _async_register_services(hass)
    
    return True


async def _async_register_services(hass: HomeAssistant) -> None:
    """Register integration services."""
    
    async def async_handle_add_event(call: ServiceCall) -> None:
        """Handle the add_event service call."""
        event_type = call.data[ATTR_TYPE]
        title = call.data[ATTR_TITLE]
        text = call.data[ATTR_TEXT]
        image = call.data.get(ATTR_IMAGE)
        camera_entity = call.data.get(ATTR_CAMERA_ENTITY)
        timestamp = call.data.get(ATTR_TIMESTAMP)
        priority = call.data.get(ATTR_PRIORITY, "normal")
        
        # Get the first configured entry
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            raise HomeAssistantError("Daily Activity Feed integration not configured")
        
        entry = entries[0]
        addon_url = entry.data[CONF_ADDON_URL]
        
        # Handle camera snapshot if camera_entity is provided
        if camera_entity and not image:
            try:
                # Generate unique filename
                timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"/config/www/daf_{timestamp_str}.jpg"
                
                # Take snapshot
                await hass.services.async_call(
                    "camera",
                    "snapshot",
                    {
                        "entity_id": camera_entity,
                        "filename": filename,
                    },
                    blocking=True,
                )
                
                # Set image path
                image = f"/local/daf_{timestamp_str}.jpg"
                _LOGGER.info("Camera snapshot created: %s", image)
                
            except Exception as err:
                _LOGGER.error("Failed to create camera snapshot: %s", err)
                # Continue without image
        
        # Generate timestamp if not provided
        if not timestamp:
            timestamp = datetime.now().strftime('%H:%M:%S')
        
        # Prepare payload
        payload = {
            "type": event_type,
            "title": title,
            "text": text,
            "timestamp": timestamp,
        }
        
        if image:
            payload["image"] = image
        
        if priority != "normal":
            payload["priority"] = priority
        
        # Send to add-on API
        try:
            session = async_get_clientsession(hass)
            url = f"{addon_url}/api/event"
            
            async with async_timeout.timeout(10):
                async with session.post(url, json=payload) as response:
                    if response.status not in (200, 201):
                        error_text = await response.text()
                        raise HomeAssistantError(
                            f"Failed to add event: HTTP {response.status} - {error_text}"
                        )
                    
                    _LOGGER.info(
                        "Event added successfully: %s - %s", event_type, title
                    )
                    
        except aiohttp.ClientError as err:
            raise HomeAssistantError(f"Connection error: {err}") from err
        except asyncio.TimeoutError as err:
            raise HomeAssistantError(f"Request timeout: {err}") from err
        except Exception as err:
            raise HomeAssistantError(f"Unexpected error: {err}") from err
    
    # Register the service with inline field definitions
    hass.services.async_register(
        DOMAIN,
        SERVICE_ADD_EVENT,
        async_handle_add_event,
        schema=SERVICE_ADD_EVENT_SCHEMA,
    )
    
    _LOGGER.info("Service 'add_event' registered successfully")


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        
        # Unregister services if no more entries
        if not hass.config_entries.async_entries(DOMAIN):
            hass.services.async_remove(DOMAIN, SERVICE_ADD_EVENT)
            _LOGGER.info("Service 'add_event' unregistered")
    
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
