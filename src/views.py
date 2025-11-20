from typing import Any

from dotenv import load_dotenv
import os
import json

from src.utils import time_for_greeting, get_data_time

load_dotenv()


def main_page(date_time:str) -> dict[str, Any]:
    """ принимает текущее время и ыормирует json приветствие для главной страницы"""

    greeting = time_for_greeting()
    time_period = get_data_time(date_time)
    sorted_df = get_path_and_period("./data/operations.xlsx", time_period)


    data_main_page = {
        "greeting": greeting
    }
    json_data = json.dumps(data_main_page, ensure_ascii=False, indent=4)


    return json_data


