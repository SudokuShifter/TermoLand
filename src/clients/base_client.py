from abc import ABC
from typing import Any, Optional

from aiohttp import ClientSession
from urllib.parse import urlencode


class BaseHTTPClient(ABC):
    @staticmethod
    async def execute_request(
        url: str,
        body: Optional[dict[str, Any]] = None,
        url_params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
        method: str = "GET",
    ) -> tuple[Any, int]:
        if headers is None:
            headers = {"Content-Type": "application/json", "accept": "application/json"}

        if method.upper() in ("GET", "HEAD") and body is not None:
            raise ValueError(f"Метод {method} не может содержать тело запроса")

        if url_params:
            url = f"{url}?{urlencode(url_params)}"

        async with ClientSession() as session:
            if method.upper() == "GET":
                response = await session.get(url, headers=headers)
            elif method.upper() == "POST":
                response = await session.post(url, json=body, headers=headers)
            elif method.upper() == "PUT":
                response = await session.put(url, json=body, headers=headers)
            elif method.upper() == "DELETE":
                response = await session.delete(url, headers=headers)
            else:
                raise ValueError(f"Неподдерживаемый метод: {method}")

            try:
                response_data = await response.json()
            except:
                response_data = await response.text()

            return response_data
