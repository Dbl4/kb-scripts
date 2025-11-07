# tests/conftest.py
import pytest


@pytest.fixture
def user_data():
    return {"name": "Alice", "role": "admin"}
