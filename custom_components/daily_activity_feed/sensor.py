"""Sensor platform for Daily Activity Feed"""
import logging
from datetime import timedelta
import aiohttp
import async_timeout

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)

DOMAIN = "daily_activity_feed"
SCAN_INTERVAL = timedelta(seconds=30)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Daily Activity Feed sensors."""
    
    addon_url = hass.data[DOMAIN].get("addon_url", "http://addon-daily-activity-feed:8099")
    
    sensors = [
        DailyActivityFeedSensor(hass, addon_url, "today", "Today"),
        DailyActivityFeedSensor(hass, addon_url, "yesterday", "Yesterday"),
    ]
    
    async_add_entities(sensors, True)


class DailyActivityFeedSensor(SensorEntity):
    """Representation of a Daily Activity Feed Sensor."""

    def __init__(self, hass: HomeAssistant, addon_url: str, day: str, name_suffix: str):
        """Initialize the sensor."""
        self.hass = hass
        self._addon_url = addon_url
        self._day = day
        self._name = f"Daily Activity {name_suffix}"
        self._state = 0
        self._attributes = {
            "entries": [],
            "last_updated": None
        }
        self._available = True

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return f"daily_activity_feed_{self._day}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:format-list-bulleted"

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        try:
            url = f"{self._addon_url}/api/events/{self._day}"
            
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.json()
                            self._state = data.get("count", 0)
                            self._attributes = {
                                "entries": data.get("events", []),
                                "date": data.get("date"),
                                "last_updated": dt_util.now().isoformat()
                            }
                            self._available = True
                        else:
                            _LOGGER.error(f"Error fetching data: HTTP {response.status}")
                            self._available = False
        
        except aiohttp.ClientError as err:
            _LOGGER.error(f"Error connecting to addon: {err}")
            self._available = False
        
        except Exception as err:
            _LOGGER.error(f"Unexpected error: {err}")
            self._available = False