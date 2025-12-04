import pytest
from datetime import datetime
from unittest.mock import patch

from src.utils import (
    time_for_greeting,
)


def test_time_for_greeting_morning():
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now().hour = 7
        assert time_for_greeting() == "Доброе утро"


def test_time_for_greeting_day():
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now().hour = 15
        assert time_for_greeting() == "Добрый день"


def test_time_for_greeting_evening():
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now().hour = 20
        assert time_for_greeting() == "Добрый вечер"


def test_time_for_greeting_night():
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now().hour = 23
        assert time_for_greeting() == "Доброй ночи"


def test_time_for_greeting_early_morning():
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now().hour = 3
        assert time_for_greeting() == "Доброй ночи"
