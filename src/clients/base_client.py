from abc import ABC
from typing import Any, Optional, Dict, Tuple, Union

from aiohttp import ClientSession
from urllib.parse import urlencode, quote
from loguru import logger


class BaseHTTPClient(ABC):
    @staticmethod
    async def execute_request(
        url: str,
        body: Optional[Dict[str, Any]] = None,
        url_params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        method: str = "GET",
    ) -> Union[Dict[str, Any], str, None]:
        """
        Выполняет HTTP-запрос к внешнему API.
        Возвращает данные ответа (dict или str) либо None в случае ошибки.
        """
        if headers is None:
            headers = {"Content-Type": "application/json", "accept": "application/json"}

        if method.upper() in ("GET", "HEAD") and body is not None:
            raise ValueError(f"Метод {method} не может содержать тело запроса")

        if url_params:
            url = f"{url}?{BaseHTTPClient.custom_urlencode(url_params)}"
        logger.info(f'Запрос отправляется на URL - {url}')
        try:
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
                except Exception as e:
                    logger.warning(f"Ответ не JSON: {e}, пытаюсь получить как текст.")
                    response_data = await response.text()

                return response_data
        except Exception as e:
            logger.error(f"Ошибка при выполнении HTTP-запроса: {e}")
            return None

    @staticmethod
    def custom_urlencode(params: dict) -> str:
        parts = []
        for key, value in params.items():
            if key == "objects":
                parts.append(f"{key}={value}")
            else:
                parts.append(f"{key}={quote(str(value))}")
        return "&".join(parts)
