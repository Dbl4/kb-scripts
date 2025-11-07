from sqlalchemy.engine.reflection import cache


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value):
        self.value = value


if __name__ == '__main__':
    # # Создание объектов
    singleton1 = Singleton(10)
    singleton2 = Singleton(20)

    # Вывод параметров
    print(singleton1.value)  # Выведет: 20
    print(singleton2.value)  # Выведет: 20