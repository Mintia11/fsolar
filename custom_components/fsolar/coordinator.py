"""DataUpdateCoordinator for FelicitySolar integration."""

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import FSolarApiClient, FSolarApiError
from .const import CONF_PASSWORD, CONF_USERNAME, DOMAIN

_LOGGER = logging.getLogger(__name__)


class FSolarDataUpdateCoordinator(DataUpdateCoordinator[dict]):
    """Class to manage fetching FSolar data."""

    def __init__(self, hass: HomeAssistant, entry_data: dict) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )
        self.entry_data = entry_data
        self.client = FSolarApiClient(async_get_clientsession(hass))

    async def _async_update_data(self) -> dict:
        """Fetch data from FSolar API."""
        try:
            if not self.client._token:
                await self.client.login(
                    self.entry_data[CONF_USERNAME], self.entry_data[CONF_PASSWORD]
                )

            plants = await self.client.get_plants()
            data = {"plants": plants, "devices": {}}

            for plant in plants:
                devices = await self.client.get_all_devices(plant.id)
                for dev in devices:
                    await self.client.get_device_data(dev)
                    # Convert device into specific typed object if applicable
                    typed_dev = dev.as_inverter() or dev.as_battery_pack() or dev
                    data["devices"][dev.device_sn] = typed_dev

            return data
        except FSolarApiError as err:
            if "401" in str(err) or "token" in str(err).lower():
                raise ConfigEntryAuthFailed from err
            raise UpdateFailed(f"Error communicating with API: {err}") from err
