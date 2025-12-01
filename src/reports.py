import json
import pandas as pd
from pandas import DataFrame

def spending_by_category(transactions: pd.DataFrame, category: str, date: str) -> dict:
    """Функция принимает датафрейм и
    возвращает траты по заданной категории
    за последние три месяца от переданной даты"""


    print(transactions)



