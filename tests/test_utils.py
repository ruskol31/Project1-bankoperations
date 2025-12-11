from unittest.mock import MagicMock, Mock, mock_open, patch

import pandas as pd
import pytest

# import tempfile
# import os
from src.utils import (cards_with_expenses, get_currency, get_data_time,
                       get_path_and_period, get_top_transaction,
                       get_user_stocks_price, time_for_greeting)


@pytest.fixture
def mock_datetime_fixture():
    """Фикстура для мока datetime"""
    with patch('src.utils.datetime') as mock_datetime:
        yield mock_datetime


def test_morning_with_fixture(mock_datetime_fixture):
    """Тест с фикстурой"""
    mock_datetime_fixture.now.return_value = Mock(hour=7)
    assert time_for_greeting() == "Доброе утро"


def test_night_with_fixture(mock_datetime_fixture):
    """Тест ночного приветствия с фикстурой"""
    mock_datetime_fixture.now.return_value = Mock(hour=2)
    assert time_for_greeting() == "Доброй ночи"


def test_day_with_fixture(mock_datetime_fixture):
    """Тест дневного приветствия с фикстурой"""
    mock_datetime_fixture.now.return_value = Mock(hour=14)
    assert time_for_greeting() == "Добрый день"


def test_get_data_time():
    """Базовый тест с датой в середине месяца"""
    date_time = "2023.10.15 14:30:45"
    result = get_data_time(date_time, "%Y.%m.%d %H:%M:%S")

    expected = [
        "01.10.2023 14:30:45",  # start_date (первое число месяца)
        "15.10.2023 14:30:45"  # оригинальная дата
    ]

    assert result == expected


def test_get_path_and_period_basic():
    """Базовый тест функции get_path_and_period с использованием моков"""

    # Создаем тестовые данные в формате DataFrame
    test_data = {
        "Дата операции": ["15.10.2023", "10.10.2023", "20.10.2023", "05.10.2023", "25.10.2023", "01.11.2023"],
        "Сумма операции": [1000, 2000, 3000, 4000, 5000, 6000],
        "Категория": ["Еда", "Транспорт", "Развлечения", "Еда", "Транспорт", "Развлечения"],
        "Описание": ["Обед", "Такси", "Кино", "Продукты", "Метро", "Концерт"]
    }

    # Создаем DataFrame из тестовых данных
    mock_df = pd.DataFrame(test_data)

    # Мокаем pd.read_excel чтобы он возвращал наш mock_df
    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.return_value = mock_df

        # Задаем период для фильтрации (только октябрь)
        period_date = ["01.10.2023 00:00:00", "31.10.2023 23:59:59"]

        # Вызываем тестируемую функцию с любым путем (он будет замокан)
        result = get_path_and_period("dummy_path.xlsx", period_date)

        # 1. Проверяем, что pd.read_excel был вызван с правильными параметрами
        mock_read_excel.assert_called_once_with(
            "dummy_path.xlsx",
            sheet_name="Отчет по операциям"
        )

        # 2. Проверяем тип результата
        assert isinstance(result, pd.DataFrame), "Функция должна возвращать DataFrame"

        # 3. Проверяем количество строк (должны быть только октябрьские операции)
        assert len(result) == 5, f"Ожидалось 5 строк, получено {len(result)}"

        # 4. Проверяем, что даты отсортированы по возрастанию
        dates_sorted = all(
            result["Дата операции"].iloc[i] <= result["Дата операции"].iloc[i + 1]
            for i in range(len(result) - 1)
        )
        assert dates_sorted, "Даты должны быть отсортированы по возрастанию"

        # 5. Проверяем, что нет ноябрьской операции
        assert result["Дата операции"].max().month == 10, "Не должно быть операций за ноябрь"

        # 6. Проверяем порядок дат после сортировки
        expected_dates = ["05.10.2023", "10.10.2023", "15.10.2023", "20.10.2023", "25.10.2023"]
        result_dates = result["Дата операции"].dt.strftime("%d.%m.%Y").tolist()
        assert result_dates == expected_dates, f"Неверный порядок дат: {result_dates}"

        # 7. Проверяем, что все колонки сохранились
        expected_columns = ["Дата операции", "Сумма операции", "Категория", "Описание"]
        assert list(result.columns) == expected_columns, "Не все колонки сохранились"


def test_cards_with_expenses():
    # Создаем минимальный тестовый DataFrame
    test_df = pd.DataFrame({
        "Номер карты": ["1234****5678"],
        "Сумма операции": [-1000],
        "Кэшбэк": [10.00],
        "Сумма операции с округлением": [-1000]
    })

    # Вызываем функцию
    result = cards_with_expenses(test_df)

    # Проверяем результат
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == {
        "last_digits": "12345678",
        "total_spent": -1000,
        "cashback": -10  # -1000 // 100 = -10
    }


def test_cards_with_expenses_multiple_cards():
    """Тест с несколькими картами"""

    test_df = pd.DataFrame({
        "Номер карты": ["1111****2222", "3333****4444", "5555****6666"],
        "Сумма операции": [-1500, 500, -300],  # расход, доход, расход
        "Кэшбэк": [15.00, 5.00, 3.00],
        "Сумма операции с округлением": [-1500, 500, -300]
    })

    result = cards_with_expenses(test_df)

    # Проверяем количество
    assert len(result) == 3

    # Проверяем первую карту (расход)
    assert result[0]["last_digits"] == "11112222"
    assert result[0]["total_spent"] == -1500
    assert result[0]["cashback"] == -15

    # Вторая карта (доход) - должна остаться как оригинальная строка
    assert not isinstance(result[1], dict) or "last_digits" not in result[1]

    # Третья карта (расход)
    assert result[2]["last_digits"] == "55556666"
    assert result[2]["total_spent"] == -300
    assert result[2]["cashback"] == -3


def test_get_top_transaction_simple():
    # Создаем простой DataFrame
    test_df = pd.DataFrame({
        "Дата платежа": ["2023-10-01", "2023-10-02", "2023-10-03"],
        "Сумма платежа": [100.0, 300.0, 200.0],
        "Категория": ["А", "Б", "В"],
        "Описание": ["Описание1", "Описание2", "Описание3"]
    })

    # Получаем топ-2 транзакции
    result = get_top_transaction(test_df, 2)

    # Проверяем базовые вещи
    assert isinstance(result, list)
    assert len(result) == 2

    # Проверяем, что транзакции отсортированы по убыванию суммы
    # Первая должна быть с суммой 300.0
    assert result[0]["amount"] == "300.0"
    assert result[0]["category"] == "Б"

    # Вторая должна быть с суммой 200.0
    assert result[1]["amount"] == "200.0"
    assert result[1]["category"] == "В"

    # Проверяем формат данных (все значения конвертируются в строки)
    assert isinstance(result[0]["date"], str)
    assert isinstance(result[0]["amount"], str)
    assert isinstance(result[0]["category"], str)
    assert isinstance(result[0]["description"], str)


def test_get_top_transaction_all_transactions():
    """Тест на получение всех транзакций"""

    test_df = pd.DataFrame({
        "Дата платежа": ["2023-10-01", "2023-10-02"],
        "Сумма платежа": [1000.0, 500.0],
        "Категория": ["Категория1", "Категория2"],
        "Описание": ["Описание1", "Описание2"]
    })

    # Запрашиваем больше транзакций, чем есть
    result = get_top_transaction(test_df, 10)

    # Должны получить все 2 транзакции
    assert len(result) == 2
    # Отсортированы по убыванию: сначала 1000.0, потом 500.0
    assert result[0]["amount"] == "1000.0"
    assert result[1]["amount"] == "500.0"


def test_one_currency_success():
    """Самый простой тест: одна валюта, успешный запрос"""
    # Подготовка
    test_json = '{"user_currencies": ["USD"]}'

    with patch('builtins.open', mock_open(read_data=test_json)), \
            patch('os.getenv', return_value='test_key'), \
            patch('requests.get') as mock_get:
        # Настраиваем успешный ответ
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "query": {"from": "USD", "to": "RUB"},
            "result": 100.0
        }
        mock_get.return_value = mock_response

        # Действие
        result = get_currency("any.json")

        # Проверка
        assert result == [{"currency": "USD", "rate": "100.0"}]


def test_api_error(capsys):
    """Тест ошибки API с перехватом вывода"""
    # Подготовка
    test_json = '{"user_currencies": ["EUR"]}'

    with patch('builtins.open', mock_open(read_data=test_json)), \
            patch('os.getenv', return_value='test_key'), \
            patch('requests.get') as mock_get:
        # Настраиваем ошибку
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Server Error"
        mock_get.return_value = mock_response

        # Действие
        result = get_currency("any.json")

        # Проверка результата
        assert result == []

        # Проверка вывода в консоль
        captured = capsys.readouterr()
        assert "Ошибка для EUR: 500" in captured.out


def test_rounding():
    """Тест округления результата"""
    test_json = '{"user_currencies": ["USD"]}'

    with patch('builtins.open', mock_open(read_data=test_json)), \
            patch('os.getenv', return_value='test_key'), \
            patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "query": {"from": "USD", "to": "RUB"},
            "result": 91.45678  # Должно округлиться до 91.46
        }
        mock_get.return_value = mock_response

        result = get_currency("any.json")

        # Проверяем округление до 2 знаков
        assert result == [{"currency": "USD", "rate": "91.46"}]


def test_one_stock_success():
    """Самый простой тест: одна акция, успешный запрос"""
    # Подготовка
    test_json = '{"user_stocks": ["AAPL"]}'

    with patch('builtins.open', mock_open(read_data=test_json)), \
            patch('os.getenv', return_value='test_key'), \
            patch('requests.get') as mock_get:
        # Настраиваем успешный ответ
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "ticker": "AAPL",
            "price": 175.5
        }
        mock_get.return_value = mock_response

        # Действие
        result = get_user_stocks_price("stocks.json")

        # Проверка
        assert result == [{"stock": "AAPL", "price": "175.5"}]


def test_api2_error(capsys):
    """Тест ошибки API"""
    # Подготовка
    test_json = '{"user_stocks": ["INVALID"]}'

    with patch('builtins.open', mock_open(read_data=test_json)), \
            patch('os.getenv', return_value='test_key'), \
            patch('requests.get') as mock_get:
        # Настраиваем ошибку
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Stock not found"
        mock_get.return_value = mock_response

        # Действие
        result = get_user_stocks_price("stocks.json")

        # Проверка результата
        assert result == []

        # Проверка вывода в консоль
        captured = capsys.readouterr()
        assert "Error:" in captured.out
        assert "404" in captured.out
