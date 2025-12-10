import logging
from typing import Any
# import pandas as pd
from dotenv import load_dotenv
# import os
import json

from src.utils import (
    time_for_greeting,
    get_data_time,
    get_path_and_period,
    cards_with_expenses,
    get_top_transaction,
    get_currency,
    get_user_stocks_price
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - MAIN_PAGE - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()


def main_page(date_time: str) -> dict[str, Any]:
    """ принимает текущее время и ыормирует json приветствие для главной страницы"""

    logger.info(f"Запуск main_page с date_time={date_time}")
    # получение датафрейма - срез из исходных данных по датам
    logger.debug("Получение периода анализа")
    time_period = get_data_time(date_time, "%Y.%m.%d %H:%M:%S")
    logger.debug("Загрузка данных операций")
    sorted_df = get_path_and_period(r'C:\pytnon\Project1 bankoperations\data\operations.xlsx', time_period)
    logger.info(f"Загружено {len(sorted_df)} операций")
    # приветствие
    greeting = time_for_greeting()
    # По каждой карте:
    cards = cards_with_expenses(sorted_df)
    # Топ-5 транзакций по сумме платежа.
    top_5_transaction = get_top_transaction(sorted_df, 5)
    # Курс валют пользователя
    currency = get_currency(r"C:\pytnon\Project1 bankoperations\data\user_settings.json")
    # Курс акций пользователя
    stock_prices = get_user_stocks_price(r"C:\pytnon\Project1 bankoperations\data\user_settings.json")
    logger.debug(f"Собраны данные: карт={len(cards)}, транзакций={len(top_5_transaction)}, "
                 f"валют={len(currency)}, акций={len(stock_prices)}")

    data = {
        "greeting": greeting,
        "cards": f"{cards}",
        "top_transactions": top_5_transaction,
        "currency": currency,
        "stock_prices": stock_prices
    }
    # print(type(greeting), type(cards), type(top_5_transaction),type(currency), type(stock_prices))
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    #
    logger.info("main_page успешно завершена")
    return json_data
