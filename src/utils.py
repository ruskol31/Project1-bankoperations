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


def get_data_time(date_time: str, date_format: "%Y.%m.%d %H:%M.%S") -> list[str]:
    dt = datetime.strptime(date_time, date_format)
    start_date = dt.replace(day=1)

    return [
        start_date.strftime("%Y.%m.%d %H:%M.%S"),
        dt.strftime("%Y.%m.%d %H:%M.%S")
    ]

def get_path_and_period(path_to_file: str, period_date: list) -> DataFrame:

def read_financial_operations_exel(file_path):
    """
    :param file_path: принимает на вход путь до exel-файла и
    :return: список словарей с данными о финансовых транзакциях
    """

    df = pd.read_excel(file_path)
    operations = df.to_dict(orient='records')

    return operations

def get_500_company_tickers() -> list:
    api_url = 'https://api.api-ninjas.com/v1/sp500'
    response = requests.get(api_url, headers={'X-Api-Key': 'iI019ChSxoTeg94zTqiChw==QhpFM6wBFh70ftUg'})
    if response.status_code == 200:
        data = response.json()
        return [item["ticker"] for item in data]
    else:
        print("Ошибка получения тикеров:", response.status_code, response.text)
        return []


def get_user_stocks_price(user_stocks):
    responses = []
    api_key = os.getenv("API_KEY1")  # Получаешь ключ из .env
    if not api_key:
        print("Ошибка: API_KEY1 не найден в .env")
    for stock in user_stocks:
        api_url = 'https://api.api-ninjas.com/v1/stockprice?ticker={}'.format(stock)
        response = requests.get(api_url, headers={'X-Api-Key': api_key})
        if response.status_code == requests.codes.ok:
            # print(response.text)
            responses.append(response.text)
        else:
            print("Error:", response.status_code, response.text)
    return responses

#
# if __name__ == "__main__":
#     # print(get_500_company_tickers())
#     user_stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
#     print(get_user_stocks_price(user_stocks))


# if __name__ == "__main__":
    # print(time_for_greeting())
    #  operations = read_financial_operations_exel(r'C:\pytnon\Project1 bankoperations\data\operations.xlsx')
    #  for op in operations:
    #      print(operations)


