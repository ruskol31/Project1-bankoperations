import json
import os
from typing import List, Dict

import requests
import pandas as pd
from datetime import datetime
from pandas import DataFrame


def time_for_greeting():
    """
    возвращает приветствие в зависимости от времени обращения пользователя

    """
    user_request_time = datetime.now().hour
    if 5 <= user_request_time <= 12:
        return "Доброе утро"
    elif 12 <= user_request_time <= 18:
        return "Добрый день"
    elif 18 <= user_request_time <= 22:
        return "Добрый вечер"
    else:
        return "Доброq ночи"


def get_data_time(date_time: str, date_format: "%Y.%m.%d %H:%M:%S") -> list[str]:
    """
    Принимает и форматирует текущую дату

    """
    dt = datetime.strptime(date_time, date_format)
    start_date = dt.replace(day=1)

    return [
        start_date.strftime("%d.%m.%Y %H:%M:%S"),
        dt.strftime("%d.%m.%Y %H:%M:%S")
    ]


def get_path_and_period(path_to_file: str, period_date: List[str]) -> DataFrame:
    """ принимает путь к xlx файлу и период за который рассматриваются операции
    и возвращает таблицу значений в заданном диапазоне"""

    df = pd.read_excel(path_to_file, sheet_name="Отчет по операциям")

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    start_date = datetime.strptime(period_date[0], "%d.%m.%Y %H:%M:%S")
    end_date = datetime.strptime(period_date[1], "%d.%m.%Y %H:%M:%S")

    filtered_df = df[
        (df["Дата операции"] >= start_date) &
        (df["Дата операции"] <= end_date)
        ]
    sorted_df = filtered_df.sort_values(by="Дата операции", ascending=True)
    # print(sorted_df)
    return sorted_df


def cards_with_expenses(sorted_df: DataFrame) -> List[Dict]:
    """ Принимает датафрейм, а возвращает список карт с расходами"""

    card_expense_trans = []
    card_sorted = sorted_df[
        [
            "Номер карты",
            "Сумма операции",
            "Кэшбэк",
            "Сумма операции с округлением"
        ]
    ]
    for index, row in card_sorted.iterrows():
        if row["Сумма операции"] < 0:
            last_digits = str(row["Номер карты"]).replace("*", "")
            total_expense = row["Сумма операции с округлением"]
            cashback = total_expense // 100
            row = {
                "last_digits": last_digits,
                "total_spent": total_expense,
                "cashback": cashback
            }
        card_expense_trans.append(row)
    # print(card_expense_trans)
    return card_expense_trans


def get_top_transaction(sorted_df: DataFrame, get_top) -> List[Dict]:
    """Принимает датафрейм, а возвращает топ в количестве get_top
    транзакций по сумме платежа"""
    top_pay_transaction = []
    sorted_pat_df = sorted_df.sort_values(by="Сумма платежа", ascending=False)
    top_transaction = sorted_pat_df.head(get_top)
    top_transaction_sorted = top_transaction[
        [
            "Дата платежа",
            "Сумма платежа",
            "Категория",
            "Описание"
        ]
    ]
    for index, row in top_transaction_sorted.iterrows():
        transaction = {
            "date": f"{row['Дата платежа']}",
            "amount": f"{row['Сумма платежа']}",
            "category": f"{row['Категория']}",
            "description": f"{row['Описание']}"
        }
        top_pay_transaction.append(transaction)

    return top_pay_transaction


def get_currency(path_to_json: str) -> list[dict]:
    """
    Функция принимает га вход путь к файлу со списком валют
     и выдает их курс на текущую дату
    """
    URL = "https://api.apilayer.com/exchangerates_data/convert"
    currency_rates = []
    API_KEY = os.getenv("API_KEY")

    with open(path_to_json, "r", encoding="utf-8") as file:
        data = json.load(file)
        currences = data['user_currencies']

        for currence in currences:
            params = {
                "amount": 1,
                "from": f"{currence}",
                "to": "RUB"
            }
            headers = {
                "apikey": f"{API_KEY}"
            }
            response = requests.get(URL, headers=headers, params=params)

            status_code = response.status_code
            if status_code == 200:
                result = response.json()
                currency_code_response = result["query"]["from"]
                currency_amount = round(result['result'], 2)
                currency_rates.append({
                    "currency": f"{currency_code_response}",
                    "rate": f"{currency_amount}"
                })
            else:
                print(f"Ошибка для {currence}: {response.status_code} - {response.text}")
        return currency_rates


# def get_500_company_tickers() -> list:
#     api_url = 'https://api.api-ninjas.com/v1/sp500'
#     response = requests.get(api_url, headers={'X-Api-Key': 'iI019ChSxoTeg94zTqiChw==QhpFM6wBFh70ftUg'})
#     if response.status_code == 200:
#         data = response.json()
#         return [item["ticker"] for item in data]
#     else:
#         print("Ошибка получения тикеров:", response.status_code, response.text)
#         return []


def get_user_stocks_price(path_to_json: str) -> list[dict]:
    """
    Принимает путь к файлу с названиями акций пользователя и возвращает их стоимость

    """
    responses = []
    api_key = os.getenv("API_KEY1")  # Получаешь ключ из .env
    if not api_key:
        print("Ошибка: API_KEY1 не найден в .env")

    with open(path_to_json, "r", encoding="utf-8") as file:
        data = json.load(file)
        user_stocks = data['user_stocks']
        for stock in user_stocks:
            api_url = 'https://api.api-ninjas.com/v1/stockprice?ticker={}'.format(stock)
            response = requests.get(api_url, headers={'X-Api-Key': api_key})
            if response.status_code == requests.codes.ok:
                result = response.json()
                stock_ticker = result["ticker"]
                price = round(result['price'], 2)
                responses.append({
                    "stock": f"{stock_ticker}",
                    "price": f"{price}"
                })
            else:
                print("Error:", response.status_code, response.text)
    return responses

#
# if __name__ == "__main__":
#     # print(get_500_company_tickers())
#     user_stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
#     print(get_user_stocks_price(user_stocks))


# if __name__ == "__main__":
#     print(time_for_greeting())
#     period_date = get_data_time
#     operations = get_path_and_period(r'C:\pytnon\Project1 bankoperations\data\operations.xlsx', period_date)
#     for op in operations:
#         print(operations)
