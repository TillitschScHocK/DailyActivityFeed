"""Sensor platform for Daily Activity Feed"""
import logging
from datetime import timedelta
import aiohttp
import async_timeout

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    CONF_ADDON_URL,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    SENSOR_TODAY,
    SENSOR_YESTERDAY,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Daily Activity Feed sensors based on a config entry."""
    
    addon_url = entry.data[CONF_ADDON_URL]
    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    
    # Create coordinators for today and yesterday
    coordinator_today = DailyActivityFeedDataUpdateCoordinator(
        hass,
        addon_url,
        SENSOR_TODAY,
        scan_interval,
    )
    
    coordinator_yesterday = DailyActivityFeedDataUpdateCoordinator(
        hass,
        addon_url,
        SENSOR_YESTERDAY,
        scan_interval,
    )
    
    # Fetch initial data
    await coordinator_today.async_config_entry_first_refresh()
    await coordinator_yesterday.async_config_entry_first_refresh()
    
    # Create sensor entities
    sensors = [
        DailyActivityFeedSensor(coordinator_today, entry, SENSOR_TODAY, "Today"),
        DailyActivityFeedSensor(coordinator_yesterday, entry, SENSOR_YESTERDAY, "Yesterday"),
    ]
    
    async_add_entities(sensors)


class DailyActivityFeedDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Daily Activity Feed data."""

    def __init__(
        self,
        hass: HomeAssistant,
        addon_url: str,
        day: str,
        scan_interval: int,
    ) -> None:
        """Initialize."""
        self.addon_url = addon_url
        self.day = day
        
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{day}",
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            url = f"{self.addon_url}/api/events/{self.day}"
            
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status != 200:
                            raise UpdateFailed(f"Error fetching data: HTTP {response.status}")
                        
                        data = await response.json()
                        return data
        
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error connecting to addon: {err}")
        
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}")


class DailyActivityFeedSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Daily Activity Feed Sensor."""

    def __init__(
        self,
        coordinator: DailyActivityFeedDataUpdateCoordinator,
        entry: ConfigEntry,
        day: str,
        name_suffix: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        
        self._day = day
        self._attr_name = f"Daily Activity {name_suffix}"
        self._attr_unique_id = f"{entry.entry_id}_{day}"
        self._attr_icon = "mdi:format-list-bulleted"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get("count", 0)
        return 0

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data:
            return {
                "entries": [],
                "date": None,
                "last_updated": None,
            }
        
        return {
            "entries": self.coordinator.data.get("events", []),
            "date": self.coordinator.data.get("date"),
            "last_updated": dt_util.now().isoformat(),
        }
