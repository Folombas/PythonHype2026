"""Сохранение персонального профиля в текстовый файл."""

import datetime
from pathlib import Path


PROFILES_DIR = Path("profiles")


def build_profile_text(name, bday, info, extras):
    """Собирает текстовый отчёт обо всех расчётах."""
    lines = []
    lines.append("=" * 50)
    lines.append(f"  Персональный профиль: {name}")
    lines.append(f"  Сохранено: {datetime.datetime.now():%d.%m.%Y %H:%M}")
    lines.append("=" * 50)
    lines.append("")

    lines.append(f"Дата рождения: {bday:%d.%m.%Y}")
    lines.append(f"Возраст: {info['years']} лет")
    lines.append(f"День недели: {info['weekday']}")
    lines.append(f"Знак зодиака: {info['zodiac']}")
    lines.append("")

    lines.append(f"🌟 Предсказание: {extras.get('prediction', '—')}")
    lines.append(f"🔢 Число жизненного пути: {extras.get('life_path', '—')}")
    lines.append(f"📅 Число дня: {extras.get('day_num', '—')}")
    lines.append(f"🐲 Восточный календарь: {extras.get('eastern', '—')}")
    lines.append(f"👥 Поколение: {extras.get('generation', '—')}")

    moon = extras.get("moon")
    if moon:
        lines.append("")
        lines.append("🌙 Лунная фаза:")
        lines.append(f"   При рождении: {moon['bday_emoji']} "
                     f"{moon['bday_name']} "
                     f"({moon['bday_illumination']:.0f}%)")
        lines.append(f"   Сегодня:      {moon['today_emoji']} "
                     f"{moon['today_name']} "
                     f"({moon['today_illumination']:.0f}%)")

    compat = extras.get("compatibility")
    if compat:
        lines.append(f"💘 Совместимость с {compat['other']}: "
                     f"{compat['percent']}% — {compat['verdict']}")

    horo = extras.get("city_horo")
    if horo:
        lines.append("")
        lines.append(f"🏡 Родной город: {horo['city']}")
        lines.append(f"   Характер: {horo['vibe']}")
        lines.append(f"   Стихия: {horo['element'][0]} — "
                     f"{horo['element'][1]}")
        lines.append(f"   Сакральное число: {horo['sacred']} "
                     f"— {horo['sacred_meaning']}")

    units = extras.get("units")
    if units:
        lines.append("")
        lines.append("⏳ Жизнь в разных единицах:")
        lines.append(f"   Дней:          {units['days']:,}".replace(",", " "))
        lines.append(f"   Часов:         {units['hours']:,}".replace(",", " "))
        lines.append(f"   Минут:         {units['minutes']:,}".replace(",", " "))
        lines.append(f"   Секунд:        {units['seconds']:,}".replace(",", " "))
        lines.append(f"   Ударов сердца: {units['heartbeats']:,}".replace(",", " "))
        lines.append(f"   Вдохов:        {units['breaths']:,}".replace(",", " "))
        lines.append(f"   Дней во сне:   {units['sleep_days']:,}".replace(",", " "))

    lines.append("")
    lines.append("=" * 50)
    return "\n".join(lines)


def save_profile(name, text):
    """Сохраняет профиль в profiles/<имя>_<дата>.txt. Возвращает путь."""
    PROFILES_DIR.mkdir(exist_ok=True)
    safe_name = "".join(c for c in name if c.isalnum() or c in "-_") or "user"
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = PROFILES_DIR / f"{safe_name}_{stamp}.txt"
    path.write_text(text, encoding="utf-8")
    return path
