from src.common.config import AppConfig
from src.clients.base_client import BaseHTTPClient
from src.services.excel_service import ExcelService

app_config = AppConfig.create()
base_http_client = BaseHTTPClient()
excel_service = ExcelService(
    http_client=base_http_client, config=app_config.external_api
)
