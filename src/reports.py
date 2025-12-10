import functools
import logging
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('finance_analytics.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


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
            logger.info(f"Отчет сохранён в файл: {file_name}")
            logger.info(f"Размер отчета: {len(result)} строк")
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
        logger.debug(f"Дата не указана, используется текущая: {date}")
    # Приводим дату к datetime
    reference_date = pd.to_datetime(date, dayfirst=True)
    transactions = transactions.copy()
    try:

        transactions["Дата операции"] = pd.to_datetime(
            transactions["Дата операции"],
            dayfirst=True,
            errors='coerce'
        )
        logger.debug(f"Дата для анализа: {reference_date}")
    except Exception as e:
        logger.error(f"Ошибка преобразования даты: {e}")
        print(f"Ошибка преобразования даты: {e}")
    # Фильтруем транзакции за последние 3 месяца
    three_months_ago = reference_date - timedelta(days=90)
    logger.debug(f"Период анализа: с {three_months_ago} по {reference_date}")
    filtered = transactions[
        (transactions["Дата операции"] >= three_months_ago) &
        (transactions["Дата операции"] <= reference_date) &
        (transactions["Категория"] == category)
    ]
    logger.info(f"Найдено {len(filtered)} транзакций по категории '{category}'")

    return filtered
