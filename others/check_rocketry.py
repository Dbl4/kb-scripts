import datetime

from rocketry import Rocketry
from rocketry.conditions.api import cron

app = Rocketry(execution="async")


@app.task(cron("25 * * * *"))
def my_func():
    # Получаем текущее время
    current_time = datetime.datetime.now()

    # Форматируем время в строку
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print("Текущее время:", formatted_time)


if __name__ == "__main__":
    app.run()
