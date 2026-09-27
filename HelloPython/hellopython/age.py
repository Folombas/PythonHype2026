"""Расчёт возраста."""
import datetime
from .zodiac import zodiac_sign

DAY_NAMES = ["понедельник", "вторник", "среда", "четверг",
             "пятница", "суббота", "воскресенье"]

def age_info(bday):
    today = datetime.date.today()
    years = today.year - bday.year
    if (today.month, today.day) < (bday.month, bday.day):
        years -= 1
    days_lived = (today - bday).days
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
