import pandas as pd
from datetime import datetime


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

def read_financial_operations_exel(file_path):
    """
    :param file_path: принимает на вход путь до exel-файла и
    :return: список словарей с данными о финансовых транзакциях
    """

    df = pd.read_excel(file_path)
    operations = df.to_dict(orient='records')

    return operations


if __name__ == "__main__":
    print(time_for_greeting())
    # operations = read_financial_operations_exel(r'C:\pytnon\Project1 bankoperations\data\operations.xlsx')
    # for op in operations:
    #     print(operations)
