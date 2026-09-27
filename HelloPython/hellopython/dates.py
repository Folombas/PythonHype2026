"""Разбор и ввод даты рождения."""
import datetime

def parse_date(s):
    for sep in (".", "/", "-"):
        if sep in s:
            parts = s.split(sep)
            break
    else:
        return None
    if len(parts) != 3:
        return None
    try:
        d, m, y = (int(p.strip()) for p in parts)
        return datetime.date(y, m, d)
    except ValueError:
        return None

def ask_birth_date():
    today = datetime.date.today()
    while True:
        raw = input("Введите дату рождения (ДД.ММ.ГГГГ): ").strip()
        bday = parse_date(raw)
        if bday is None:
            print("  Ошибка формата. Пример: 30.11.1987")
        elif bday > today:
            print("  Дата рождения не может быть в будущем!")
        else:
            return bday
