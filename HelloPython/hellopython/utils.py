"""Вспомогательные функции: склонения и форматирование."""

def plural_years(n):
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
    n = abs(n)
    if 11 <= n % 100 <= 14:
        return "дней"
    last = n % 10
    if last == 1:
        return "день"
    if last in (2, 3, 4):
        return "дня"
    return "дней"

def format_big_number(n):
    return f"{n:,}".replace(",", " ")
