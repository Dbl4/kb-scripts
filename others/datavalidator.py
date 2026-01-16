import time
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union

Rule = Union[Callable[[Any], Any], List[Callable[[Any], Any]]]

class ValidationError(Exception):
    def __init__(self, field: str, message: str, original_value: Any = None):
        self.field = field
        self.message = message
        self.original_value = original_value
        super().__init__(f"Field '{field}': {message} (value: {original_value})")

class DataValidator:
    def __init__(self, rules: Dict[str, Rule]):
        self.rules = rules

    def __enter__(self):
        # Можно инициализировать ресурсы, например, подключение к БД для валидации
        print("Starting validation session")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Можно закрывать ресурсы или логировать завершение
        print("Validation session ended")
        # Если вернуть True, исключение будет подавлено
        return False

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {}
        for field, value in data.items():
            try:
                if field in self.rules:
                    result[field] = self._apply_rules(field, value)
                else:
                    result[field] = value
            except ValidationError as e:
                # Поднимаем исключение дальше, но можно добавить доп. информацию
                raise
            except Exception as e:
                # Обертываем любые другие исключения в ValidationError
                raise ValidationError(
                    field=field,
                    message=f"Unexpected error: {str(e)}",
                    original_value=value
                )
        return result

    def _apply_rules(self, field: str, value: Any) -> Any:
        """Применяет правила к значению поля"""
        rules = self.rules[field]

        # Приводим к списку для единообразной обработки
        if not isinstance(rules, list):
            rules = [rules]

        current_value = value
        for rule in rules:
            try:
                current_value = rule(current_value)
            except ValidationError:
                # Пробрасываем ValidationError дальше
                raise
            except Exception as e:
                # Обертываем другие исключения
                raise ValidationError(
                    field=field,
                    message=f"Rule {rule.__name__} failed: {str(e)}",
                    original_value=value
                )

        return current_value

# Правила валидации
def rule_int(value: Any) -> int:
    """Преобразует значение в целое число"""
    if value is None:
        raise ValidationError(
            field="unknown",  # Поле будет уточнено в DataValidator
            message="Cannot convert None to int",
            original_value=value
        )
    try:
        return int(value)
    except (ValueError, TypeError) as e:
        raise ValidationError(
            field="unknown",
            message=f"Cannot convert to int: {str(e)}",
            original_value=value
        )

def rule_str_to_lower(value: Any) -> str:
    """Приводит строку к нижнему регистру"""
    if not isinstance(value, str):
        raise ValidationError(
            field="unknown",
            message=f"Expected string, got {type(value).__name__}",
            original_value=value
        )
    return value.lower()

def rule_range(value: int) -> List[int]:
    """Создает список range(value)"""
    if not isinstance(value, int):
        raise ValidationError(
            field="unknown",
            message=f"Expected int for range, got {type(value).__name__}",
            original_value=value
        )
    if value < 0:
        raise ValidationError(
            field="unknown",
            message="Value must be non-negative for range",
            original_value=value
        )
    return list(range(value))

# Декоратор для логгирования и тайминга
def log_validation(func):
    """Декоратор для логирования вызовов validate"""
    @wraps(func)
    def wrapper(self, data: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[LOG] Starting validation of {len(data)} fields")
        start_time = time.time()

        try:
            result = func(self, data)
            elapsed = time.time() - start_time
            print(f"[LOG] Validation completed successfully in {elapsed:.4f}s")
            return result
        except ValidationError as e:
            elapsed = time.time() - start_time
            print(f"[LOG] Validation failed after {elapsed:.4f}s: {str(e)}")
            raise

    return wrapper

# Использование
if __name__ == "__main__":
    rules = {
        'age': rule_int,
        'score': [rule_int, rule_range],
        'email': rule_str_to_lower,
        'name': rule_str_to_lower
    }

    # Применяем декоратор к методу
    DataValidator.validate = log_validation(DataValidator.validate)

    data = {
        'age': '25',
        'score': '5',
        'email': 'Test@Example.COM',
        'name': 'John Doe'
    }

    try:
        with DataValidator(rules) as validator:
            result = validator.validate(data)
            print("Result:", result)

            # Тест с ошибкой
            invalid_data = {'age': 'not_a_number'}
            result2 = validator.validate(invalid_data)
    except ValidationError as e:
        print(f"Validation error: {e}")