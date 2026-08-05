from homeassistant.const import Platform

DOMAIN = "fsolar"
BASE_URL = "https://shine-api.felicitysolar.com"
PLATFORMS: list[Platform] = [Platform.SENSOR]

CONF_USERNAME = "username"
CONF_PASSWORD = "password"
