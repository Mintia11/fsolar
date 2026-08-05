import asyncio
from typing import Any

import aiohttp

from fsolar.consts import BASE_URL
from fsolar.device import FSolarDevice
from fsolar.plant import FSolarPlant
from fsolar.rsa import encrypt


class FSolarApiError(Exception):
    """Custom exception for FSolar API errors."""


class FSolarApiClient:
    def __init__(self, session: aiohttp.ClientSession, token: str | None = None):
        self._session = session
        self._token = token

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        auth: bool = True,
    ) -> dict[str, Any]:
        headers = {}
        if auth and self._token:
            headers["Authorization"] = f"{self._token}"

        try:
            async with self._session.request(
                method,
                f"{BASE_URL}{path}",
                json=json,
                params=params,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                data = await resp.json(content_type=None)
        except asyncio.TimeoutError as err:
            raise FSolarApiError(f"Request to {path} timed out") from err
        except aiohttp.ClientError as err:
            raise FSolarApiError(f"Request to {path} failed: {err}") from err

        if data["code"] != 200:
            raise FSolarApiError(
                f"API error {data['code']}: {data.get('message', 'No message')}"
            )

        return data

    async def login(self, username: str, password: str) -> None:
        """Logs in to the FSolar API and stores the token."""
        response = await self._request(
            "POST",
            "/app/base/userlogin",
            json={
                "userName": username,
                "password": encrypt(password),
                "version": "1.0",
            },
            auth=False,
        )
        self._token = response["data"]["token"]
        return self._token

    async def get_plants(self) -> list[FSolarPlant]:
        """Fetches the list of plants associated with the logged-in user."""
        response = await self._request(
            "POST",
            "/app/plant/list_collect_plant",
            json={"pageNum": 1, "pageSize": 100},
            auth=True,
        )
        return [FSolarPlant(plant_data) for plant_data in response["data"]["dataList"]]

    async def get_all_devices(self, plant_id: str) -> list[FSolarDevice]:
        """Fetches all devices for a given plant."""
        response = await self._request(
            "POST",
            "/app/device/list_device_all_type",
            json={"pageNum": 1, "pageSize": 100},
            auth=True,
        )
        # need to filter devices by plant_id because the API returns devices for all plants
        return [
            FSolarDevice(device)
            for device in response["data"]["dataList"]
            if device.get("plantId") == plant_id
        ]

    async def get_device_data(self, device: FSolarDevice) -> None:
        """Fetches the latest data for a given device."""
        response = await self._request(
            "POST",
            "/app/device/get_device_snapshot",
            json={
                "deviceSn": device.device_sn,
                "deviceType": device.device_type,
                "dateStr": "1",
            },
            auth=True,
        )
        device_data = response["data"]
        device.update(device_data)
