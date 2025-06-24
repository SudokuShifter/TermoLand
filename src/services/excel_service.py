import pandas as pd
import asyncio
from functools import reduce
from loguru import logger
from typing import Any, Dict, List, Optional

from src.common.const import (
    STATIC_API_RESPONSE,
    DEFAULT_DATE,
    DEFAULT_MODE,
    DEFAULT_RESULT_PATH,
)
from src.clients.base_client import BaseHTTPClient
from src.common.config import ExternalApiConfig


class ExcelService:
    def __init__(self, http_client: BaseHTTPClient, config: ExternalApiConfig):
        self.http_client = http_client
        self.config = config

    async def get_data_of_visits(
        self, exists_zones: dict, date: str = DEFAULT_DATE, mode: str = DEFAULT_MODE
    ) -> Optional[dict]:
        url_params = {
            "mode": mode,
            "date": date,
            "objects": (",").join(exists_zones),
        }
        try:
            data = await self.http_client.execute_request(
                method="GET",
                url=f"{self.config.URL}/{self.config.PATH}",
                url_params=url_params,
            )
            return data
        except Exception as e:
            logger.error(f"Ошибка при получении данных посещений: {e}")
            return None

    async def get_data_of_visits_static(self, exists_zones: dict) -> dict:
        await asyncio.sleep(0.1)  # Имитация работы внешнего сервиса
        return STATIC_API_RESPONSE

    def generate_dfs_from_response_data(
        self, response_data: dict
    ) -> Optional[pd.DataFrame]:
        list_dfs = []

        for _, title, _, statistic in response_data.get("data"):
            if not statistic or not isinstance(statistic, list):
                logger.warning(f"Пустая или некорректная статистика для {title}")
                continue
            df = pd.DataFrame(
                data=statistic, columns=["Время", f"Вход_{title}", f"Выход_{title}"]
            )
            list_dfs.append(df)

        try:
            linked_df = reduce(
                lambda left, right: pd.merge(left, right, on="Время"), list_dfs
            )
            return linked_df

        except Exception as e:
            logger.error(f"Ошибка при объединении DataFrame: {e}")
            return None

    def save_df_to_excel(self, df: pd.DataFrame, path: str = DEFAULT_RESULT_PATH):
        try:
            df.to_excel(path, index=False)
            logger.info(f"Файл успешно сохранён: {path}")

        except Exception as e:
            logger.error(f"Ошибка при сохранении Excel-файла: {e}")
