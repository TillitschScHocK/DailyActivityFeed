"""Daily Activity Feed Integration"""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

_LOGGER = logging.getLogger(__name__)

DOMAIN = "daily_activity_feed"
PLATFORMS = [Platform.SENSOR]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Daily Activity Feed component."""
    hass.data.setdefault(DOMAIN, {})
    
    # Configuration from configuration.yaml
    if DOMAIN in config:
        conf = config[DOMAIN]
        hass.data[DOMAIN] = {
            "addon_url": conf.get("addon_url", "http://addon-daily-activity-feed:8099"),
            "scan_interval": conf.get("scan_interval", 30)
        }
    else:
        hass.data[DOMAIN] = {
            "addon_url": "http://addon-daily-activity-feed:8099",
            "scan_interval": 30
        }
    
    # Forward setup to sensor platform
    await hass.helpers.discovery.async_load_platform("sensor", DOMAIN, {}, config)
    
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)