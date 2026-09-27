"""Лунная фаза при рождении и сегодня."""

import datetime


SYNODIC_MONTH = 29.530588853
KNOWN_NEW_MOON = datetime.datetime(2000, 1, 6, 18, 14)

MOON_EMOJI = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]

MOON_NAMES = [
    "Новолуние",
    "Молодая луна",
    "Первая четверть",
    "Прибывающая луна",
    "Полнолуние",
    "Убывающая луна",
    "Последняя четверть",
    "Старая луна",
]


def moon_phase(date_obj):
    """Возвращает (фаза_в_днях, эмодзи, название) для даты."""
    dt = datetime.datetime(date_obj.year, date_obj.month, date_obj.day)
    days = (dt - KNOWN_NEW_MOON).total_seconds() / 86400
    phase = days % SYNODIC_MONTH

    idx = int((phase / SYNODIC_MONTH) * 8 + 0.5) % 8
    return phase, MOON_EMOJI[idx], MOON_NAMES[idx]


def moon_illumination(phase):
    """Возвращает процент освещённости Луны (0–100)."""
    frac = phase / SYNODIC_MONTH
    if frac < 0.5:
        return frac * 200
    return (1 - frac) * 200


def moon_report(bday):
    """Возвращает словарь с информацией о Луне при рождении и сегодня."""
    bday_phase, bday_emoji, bday_name = moon_phase(bday)
    today_phase, today_emoji, today_name = moon_phase(datetime.date.today())

    return {
        "bday_emoji":        bday_emoji,
        "bday_name":         bday_name,
        "bday_illumination": moon_illumination(bday_phase),
        "today_emoji":        today_emoji,
        "today_name":         today_name,
        "today_illumination": moon_illumination(today_phase),
    }
