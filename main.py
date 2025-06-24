import asyncio

from src.common.pkg import generate_existing_zone_from_excel
from src.application import excel_service


async def main():
    exists_zone = generate_existing_zone_from_excel()
    uid_zones = list(exists_zone.keys())
    data = await excel_service.get_data_of_visits_static(uid_zones)
    df = excel_service.generate_dfs_from_response_data(data)
    excel_service.save_df_to_excel(df)


if __name__ == "__main__":
    asyncio.run(main())
