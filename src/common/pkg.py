import pandas as pd

from src.common.const import DEFAULT_FILE_PATH


def generate_existing_zone_from_excel(filename: str = DEFAULT_FILE_PATH) -> dict:
    data = {}
    df = pd.read_excel(filename)
    for uid, title in df.values:
        data[uid] = title
    return data
