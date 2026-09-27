"""Нумерология."""
import datetime

LIFE_PATH_MEANINGS = {
    1: "Лидер. Независимость, воля, первопроходец.",
    2: "Дипломат. Гармония, партнёрство, чуткость.",
    3: "Творец. Общение, радость, самовыражение.",
    4: "Строитель. Порядок, труд, надёжность.",
    5: "Свободный. Перемены, приключения, любознательность.",
    6: "Хранитель. Забота, семья, ответственность.",
    7: "Мудрец. Анализ, глубина, духовность.",
    8: "Достигатор. Власть, деньги, амбиции.",
    9: "Гуманист. Сострадание, завершение, служение.",
}

def digit_sum(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def life_path_number(bday):
    return digit_sum(bday.day + bday.month + bday.year)

def personal_day_number(bday):
    today = datetime.date.today()
    return digit_sum(life_path_number(bday) + today.day + today.month)
