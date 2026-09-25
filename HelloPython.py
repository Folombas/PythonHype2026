# HelloPython.py — интерактивное приветствие с расчётом возраста
# Демонстрирует: input, print, f-строки, функции, цикл while,
# ветвление, словарь, модуль datetime, обработку ошибок

import datetime


# ---------- Дата рождения ----------

def parse_date(s):
    """Разбирает строку 'ДД.ММ.ГГГГ' в объект date. Возвращает None при ошибке."""
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
    """Спрашивает дату рождения, пока не введена корректная."""
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


# ---------- Правильные русские окончания ----------

def plural_years(n):
    """Возвращает 'год', 'года' или 'лет' для числа n."""
    n = abs(n)
    if 11 <= n % 100 <= 14:
        return "лет"
    last = n % 10
    if last == 1:
        return "год"
    if last in (2, 3, 4):
        return "года"
    return "лет"


def plural_days(n):
    """Возвращает 'день', 'дня' или 'дней' для числа n."""
    n = abs(n)
    if 11 <= n % 100 <= 14:
        return "дней"
    last = n % 10
    if last == 1:
        return "день"
    if last in (2, 3, 4):
        return "дня"
    return "дней"
    
def zodiac_sign(day, month):
    """Возвращает знак зодиака по дню и месяцу рождения."""
    if (month == 1 and day <= 19) or (month == 12 and day >= 22):
        return "Козерог"

    signs = [
        ((1, 20), "Водолей"),
        ((2, 19), "Рыбы"),
        ((3, 21), "Овен"),
        ((4, 20), "Телец"),
        ((5, 21), "Близнецы"),
        ((6, 21), "Рак"),
        ((7, 23), "Лев"),
        ((8, 23), "Дева"),
        ((9, 23), "Весы"),
        ((10, 23), "Скорпион"),
        ((11, 22), "Стрелец"),
    ]

    for (m, d), sign in signs:
        if (month, day) < (m, d):
            return sign

    return "Стрелец"    


# ---------- Расчёт возраста ----------

DAY_NAMES = ["понедельник", "вторник", "среда", "четверг",
             "пятница", "суббота", "воскресенье"]


def age_info(bday):
    """Возвращает словарь с информацией о возрасте."""
    today = datetime.date.today()

    # Полных лет
    years = today.year - bday.year
    if (today.month, today.day) < (bday.month, bday.day):
        years -= 1

    # Прожито дней
    days_lived = (today - bday).days

    # Следующий день рождения
    next_bday = bday.replace(year=today.year)
    if next_bday < today:
        next_bday = bday.replace(year=today.year + 1)
    days_to_next = (next_bday - today).days

    return {
        "years": years,
        "days_lived": days_lived,
        "days_to_next": days_to_next,
        "weekday": DAY_NAMES[bday.weekday()],
        "zodiac": zodiac_sign(bday.day, bday.month),
    }


# ---------- Приветствия ----------

def greet(name, style, info):
    """Возвращает приветствие в выбранном стиле."""
    years = info["years"]
    suffix = plural_years(years)
    today = datetime.date.today()

    styles = {
        "1": f"Привет, {name}! Добро пожаловать в Python.",
        "2": f"Здравствуйте, {name}. Вам {years} {suffix}.",
        "3": f"Хай, {name}! 🐍 Python ждёт тебя.",
        "4": f"Салют, {name}! Сегодня {today:%d.%m.%Y}.",
        "5": (f"{name}, вы родились в {info['weekday']}, "
              f"прожили {info['days_lived']} "
              f"{plural_days(info['days_lived'])}."),
    }
    return styles.get(style, f"Привет, {name}!")


# ---------- Основная программа ----------

def main():
    print("=" * 40)
    print("   Программа HelloPython")
    print("=" * 40)

    name = input("Как вас зовут? ").strip() or "друг"
    print()
    bday = ask_birth_date()
    info = age_info(bday)

    print()
    print(f"Отлично, {name}! Вам {info['years']} "
          f"{plural_years(info['years'])}.")
    print(f"Ваш знак зодиака: {info['zodiac']}.")       
    if info["days_to_next"] == 0:
        print("🎉 С днём рождения!")
    else:
        print(f"До следующего дня рождения: {info['days_to_next']} "
              f"{plural_days(info['days_to_next'])}.")

    while True:
        print()
        print("Выберите стиль приветствия:")
        print("  1 — дружеский")
        print("  2 — с возрастом")
        print("  3 — неформальный")
        print("  4 — с датой")
        print("  5 — с днём недели и прожитыми днями")
        print("  0 — выход")

        choice = input("Ваш выбор: ").strip()

        if choice == "0":
            print(f"\nДо встречи, {name}! 👋")
            break
        elif choice in {"1", "2", "3", "4", "5"}:
            print()
            print(greet(name, choice, info))
        else:
            print("\nНет такого варианта. Попробуйте снова.")


if __name__ == "__main__":
    main()
