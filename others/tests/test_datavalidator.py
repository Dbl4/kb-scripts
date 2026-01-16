from typing import Dict, Any

import pytest

from others import datavalidator
from others.datavalidator import ValidationError, DataValidator, rule_int, rule_str_to_lower, rule_range


@pytest.mark.parametrize(
    "value, expected",
    [
        ('25', 25),
        ('0', 0),
    ]
)
def test_rule_int_valid(value, expected):
    result = datavalidator.rule_int(value)
    assert expected == result


@pytest.mark.parametrize(
    "value, error_pattern",
    [
        (None, "Cannot convert None to int"),
        ('abc', "Cannot convert to int"),
    ]
)
def test_rule_int_invalid(value, error_pattern):
    with pytest.raises(ValidationError) as ec_info:
        datavalidator.rule_int(value)

    assert error_pattern in ec_info.value.message


class TestIntegration:
    """Интеграционные тесты"""

    def test_full_workflow(self):
        """Полный рабочий процесс с контекстным менеджером"""
        rules = {
            'id': rule_int,
            'username': rule_str_to_lower
        }

        test_data = {
            'id': '100',
            'username': 'AdminUser',
            'status': 'active'  # Без правила
        }

        with DataValidator(rules) as validator:
            result = validator.validate(test_data)

            assert result['id'] == 100
            assert result['username'] == 'adminuser'
            assert result['status'] == 'active'

    def test_error_handling_in_context(self):
        """Тест обработки ошибок в контекстном менеджере"""
        rules = {'age': rule_int}
        validator = DataValidator(rules)

        # Контекстный менеджер не должен подавлять исключения
        with pytest.raises(ValidationError):
            with validator:
                validator.validate({'age': 'invalid'})


class TestDataValidator:
    """Тесты для класса DataValidator"""

    @pytest.fixture
    def sample_rules(self) -> Dict[str, Any]:
        """Фикстура с тестовыми правилами"""
        return {
            'age': rule_int,
            'score': [rule_int, rule_range],
            'email': rule_str_to_lower,
            'name': rule_str_to_lower
        }

    @pytest.fixture
    def validator(self, sample_rules) -> DataValidator:
        """Фикстура создает валидатор"""
        return DataValidator(sample_rules)

    def test_initialization(self, sample_rules):
        """Тест инициализации валидатора"""
        validator = DataValidator(sample_rules)
        assert validator.rules == sample_rules
