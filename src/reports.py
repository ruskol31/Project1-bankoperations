import json
import pandas as pd
from pandas import DataFrame
from datetime import datetime, timedelta
from typing import Optional
import functools
import os


def report_decorator(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Определяем имя файла
            if filename is None:
                # Имя по умолчанию: имя_функции_дата.csv
                date_str = datetime.now().strftime("%Y%m-%d")
                file_name = f"{func.__name__}_{date_str}.csv"
            else:
                file_name = filename

            # Сохраняем результат в файл
            result.to_csv(file_name, index=False, encoding='utf-8')
            print(f"Отчет сохранён в {file_name}")

            return result

        return wrapper

    return decorator


@report_decorator()
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние три месяца.
    Если дата не передана — используется текущая дата.
    """

    if date is None:
        date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    # Приводим дату к datetime
    reference_date = pd.to_datetime(date, dayfirst=True)
    transactions = transactions.copy()


    try:

        transactions["Дата операции"] = pd.to_datetime(
            transactions["Дата операции"],
            dayfirst=True,
            errors='coerce'
        )
    except Exception as e:
        print(f"Ошибка преобразования даты: {e}")
    # Фильтруем транзакции за последние 3 месяца
    three_months_ago = reference_date - timedelta(days=90)
    filtered = transactions[
        (transactions["Дата операции"] >= three_months_ago) &
        (transactions["Дата операции"] <= reference_date) &
        (transactions["Категория"] == category)  # предполагаем, что столбец называется "Категория"
        ]

    return filtered
