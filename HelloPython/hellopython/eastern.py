"""Восточный календарь."""

EASTERN_ANIMALS = [
    "🐀 Крыса", "🐂 Бык", "🐅 Тигр", "🐇 Кролик",
    "🐉 Дракон", "🐍 Змея", "🐎 Лошадь", "🐐 Коза",
    "🐒 Обезьяна", "🐓 Петух", "🐕 Собака", "🐖 Свинья",
]

def eastern_animal(bday):
    year = bday.year
    if (bday.month, bday.day) < (2, 20):
        year -= 1
    return EASTERN_ANIMALS[(year - 4) % 12]
