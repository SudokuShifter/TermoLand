import pandas as pd
import asyncio
from functools import reduce

from src.common.const import STATIC_API_RESPONSE
from src.clients.base_client import BaseHTTPClient
from src.common.config import ExternalApiConfig


class ExcelService:
    def __init__(self, http_client: BaseHTTPClient, config: ExternalApiConfig):
        self.http_client = http_client
        self.config = config

    async def get_data_of_visits(self, exists_zones: dict) -> dict:
        url_params = {
            "mode": "halfhour",
            "date": "3.06.2020",
            "objects": (",").join(exists_zones),
        }
        data = await self.http_client.execute_request(
            method="GET",
            url=f"{self.config.URL}/{self.config.PATH}",
            url_params=url_params,
        )
        return data

    async def get_data_of_visits_static(self, exists_zones: dict) -> dict:
        await asyncio.sleep(0.1)  # Иммитация работы внешнего сервиса
        return STATIC_API_RESPONSE

    def generate_dfs_from_response_data(
        self, response_data: dict
    ) -> list[pd.DataFrame | None]:
        list_dfs = []
        for _, title, _, statistic in response_data.get("data"):
            df = pd.DataFrame(
                data=statistic, columns=["Время", f"Вход_{title}", f"Выход_{title}"]
            )
            list_dfs.append(df)

        linked_df = reduce(
            lambda left, right: pd.merge(left, right, on="Время"), list_dfs
        )
        return linked_df

    def save_df_to_excel(self, df: pd.DataFrame, path: str = "/"):
        df.to_excel("result.xlsx")
