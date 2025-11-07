import pandas as pd


# Создаем данные для таблицы
data = {
    "Имя участника": [
        "Адмирал + жена адмирала + Максим", "Влад + Света1", "Влад + Света2",
        "Артем + Алена", "Дима", "Витяо", "Семен"
    ],
    "Наименование затрат": ["" for _ in range(7)],
    "Стоимость с человека": ["" for _ in range(7)],
    "Аванс": ["" for _ in range(7)],
    "Примечание": ["" for _ in range(7)]
}

# Создаем DataFrame
df = pd.DataFrame(data)

# Сохраняем в файл
file_path = "zatraty_na_splav.xlsx"
df.to_excel(file_path, index=False)
