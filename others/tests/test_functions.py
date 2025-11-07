import pytest
from unittest.mock import patch, mock_open, MagicMock
from others.functions_for_tests import is_palindrome, write_data, get_user_data

@pytest.mark.parametrize("word, expected", [
    ("madam", True),
    ("racecar", True),
    ("hello", False),
    ("", True),
    ("a", True),
])
def test_is_palindrome(word, expected):
    assert is_palindrome(word) == expected

def test_write_data():
    mock_file = mock_open()
    with patch("builtins.open", mock_file):
        write_data("test.txt", "Hello World")

    # Проверяем, что open вызван правильно
    mock_file.assert_called_once_with("test.txt", "w")
    # Проверяем, что write вызван с нужной строкой
    mock_file().write.assert_called_once_with("Hello World")


@patch("requests.get")
def test_get_user_data_success(mock_get):
    # Настраиваем mock для успешного ответа
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 10, "name": "Alice"}
    mock_get.return_value = mock_response

    result = get_user_data(10)

    mock_get.assert_called_once_with("https://api.example.com/users/10")
    assert result == {"id": 10, "name": "Alice"}


@patch("requests.get")
def test_get_user_data_not_found(mock_get):
    # Настраиваем mock для неуспешного ответа
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = get_user_data(999)

    mock_get.assert_called_once_with("https://api.example.com/users/999")
    assert result is None

# tests/test_users.py
def test_user_role(user_data):
    assert user_data["role"] == "admin"
