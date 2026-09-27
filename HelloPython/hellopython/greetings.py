"""Стили приветствия."""
import datetime
from .colors import Color
from .utils import plural_years, plural_days

def greet(name, style, info):
    years = info["years"]
    suffix = plural_years(years)
    today = datetime.date.today()
    C = Color
    styles = {
        "1": f"{C.GREEN}Привет, {name}! Добро пожаловать в Python.{C.RESET}",
        "2": f"{C.CYAN}Здравствуйте, {name}. Вам {years} {suffix}.{C.RESET}",
        "3": f"{C.YELLOW}Хай, {name}! 🐍 Python ждёт тебя.{C.RESET}",
        "4": f"{C.BLUE}Салют, {name}! Сегодня {today:%d.%m.%Y}.{C.RESET}",
        "5": (f"{C.PURPLE}{name}, вы родились в {info['weekday']}, "
              f"прожили {info['days_lived']} "
              f"{plural_days(info['days_lived'])}.{C.RESET}"),
    }
    return styles.get(style, f"Привет, {name}!")
