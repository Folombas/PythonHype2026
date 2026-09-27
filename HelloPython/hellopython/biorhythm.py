"""Расчёт биоритмов."""
import datetime
import math

def biorhythm(bday):
    days = (datetime.date.today() - bday).days
    return {
        "physical":     math.sin(2 * math.pi * days / 23),
        "emotional":    math.sin(2 * math.pi * days / 28),
        "intellectual": math.sin(2 * math.pi * days / 33),
    }

def render_bar(value, width=30):
    pos = int((value + 1) / 2 * (width - 1))
    bar = ["─"] * width
    bar[pos] = "●"
    return "".join(bar)
