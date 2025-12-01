import json

import pandas as pd
from datetime import datetime
from pandas import DataFrame


def cashback_analiser(file_path: str, year: int, month: int) -> dict[str, int]:
    """ нализирует выгодные ктегории кэшбека и записывает их в json  файл"""

    df = pd.read_excel(file_path)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    filtered_data = df[
        (df["Дата операции"].dt.year == year)
        &
        (df["Дата операции"].dt.month == month)
        ]

    filtered_data = filtered_data[
        (filtered_data["Кэшбэк"] > 0)
        ]

    filtered_data = filtered_data[
        filtered_data["Сумма платежа"] < 0
        ]

    expenses_by_category = filtered_data.groupby('Категория')["Сумма платежа"].sum()
    cashback_by_category = abs(expenses_by_category) // 100
    result = cashback_by_category.to_dict()
    return json.dumps(result, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    print(cashback_analiser(r'C:\pytnon\Project1 bankoperations\data\operations.xlsx', 2019, 5))