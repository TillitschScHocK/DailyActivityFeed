"""Constants for Daily Activity Feed integration."""

DOMAIN = "daily_activity_feed"

# Configuration
CONF_ADDON_URL = "addon_url"
CONF_SCAN_INTERVAL = "scan_interval"

# Defaults
DEFAULT_ADDON_URL = "http://addon-daily-activity-feed:8099"
DEFAULT_SCAN_INTERVAL = 30

# Sensor
SENSOR_TODAY = "today"
SENSOR_YESTERDAY = "yesterday"

# Services
SERVICE_ADD_EVENT = "add_event"

# Service Attributes
ATTR_TYPE = "type"
ATTR_TITLE = "title"
ATTR_TEXT = "text"
ATTR_IMAGE = "image"
ATTR_CAMERA_ENTITY = "camera_entity"
ATTR_TIMESTAMP = "timestamp"
ATTR_PRIORITY = "priority"
