from typing import Any

import pandas as pd
from dotenv import load_dotenv
import os
import json

from src.utils import time_for_greeting, get_data_time, get_path_and_period, cards_with_expenses, get_top_transaction

load_dotenv()


def main_page(date_time: str) -> dict[str, Any]:
    """ принимает текущее время и ыормирует json приветствие для главной страницы"""

    # получение датафрейма - срез из исходных данных по датам
    time_period = get_data_time(date_time, "%Y.%m.%d %H:%M:%S")
    sorted_df = get_path_and_period(r'C:\pytnon\Project1 bankoperations\data\operations.xlsx', time_period)
    # приветствие
    greeting = time_for_greeting()
    # По каждой карте:
    cards = cards_with_expenses(sorted_df)
    # Топ-5 транзакций по сумме платежа.
    top_5_transaction = get_top_transaction(sorted_df, 5)

    data = [
        "greeting": greeting,
        "cards": cards
    ]
    # data = sorted_df.to_dict(orient="records")
    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    return json_data
