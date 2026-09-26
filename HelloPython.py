# HelloPython.py — интерактивное приветствие с расчётом возраста
# Демонстрирует: input, print, f-строки, функции, цикл while,
# ветвление, словарь, модуль datetime, обработку ошибок

import datetime
import hashlib
import math


# ---------- ANSI-цвета для терминала ----------

class Color:
    """ANSI-коды для цветного вывода в терминале."""
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    PURPLE = "\033[95m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"


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


# ---------- Знак зодиака ----------

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


# ---------- Персональное предсказание ----------

def daily_prediction(name):
    """Возвращает персональное предсказание на сегодня (детерминированное)."""
    today = datetime.date.today().isoformat()
    seed = f"{name}-{today}"
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)

    predictions = [
        "Сегодня отличный день для новых начинаний.",
        "Удача улыбнётся вам в неожиданном месте.",
        "Не бойтесь экспериментировать — сегодня всё получится.",
        "Хороший день, чтобы узнать что-то новое.",
        "Обратите внимание на детали — в них скрыт ответ.",
        "Ваша энергия сегодня особенно сильна — используйте её.",
        "День подходит для тёплых разговоров с близкими.",
        "Вас ждёт приятная неожиданность.",
        "Сделайте сегодня то, что давно откладывали.",
        "Доверьтесь интуиции — она не подведёт.",
    ]
    return predictions[h % len(predictions)]


# ---------- Биоритмы ----------

def biorhythm(bday):
    """Рассчитывает биоритмы (физический, эмоциональный, интеллектуальный)."""
    days = (datetime.date.today() - bday).days
    return {
        "physical":     math.sin(2 * math.pi * days / 23),
        "emotional":    math.sin(2 * math.pi * days / 28),
        "intellectual": math.sin(2 * math.pi * days / 33),
    }


def render_bar(value, width=30):
    """Рисует горизонтальную шкалу для значения от -1 до +1."""
    pos = int((value + 1) / 2 * (width - 1))
    bar = ["─"] * width
    bar[pos] = "●"
    return "".join(bar)


# ---------- Космический возраст ----------

PLANETS = [
    ("☿ Меркурий", 0.2408467),
    ("♀ Венера",   0.61519726),
    ("♂ Марс",     1.8808158),
    ("♃ Юпитер",   11.862615),
    ("♄ Сатурн",   29.447498),
    ("⛢ Уран",     84.016846),
    ("♆ Нептун",   164.79132),
]


def cosmic_age(bday):
    """Возвращает список (планета, возраст на ней) для всех планет."""
    earth_years = (datetime.date.today() - bday).days / 365.2425
    return [(name, earth_years / period) for name, period in PLANETS]


# ---------- Восточный календарь ----------

EASTERN_ANIMALS = [
    "🐀 Крыса", "🐂 Бык", "🐅 Тигр", "🐇 Кролик",
    "🐉 Дракон", "🐍 Змея", "🐎 Лошадь", "🐐 Коза",
    "🐒 Обезьяна", "🐓 Петух", "🐕 Собака", "🐖 Свинья",
]


def eastern_animal(bday):
    """Возвращает животное восточного календаря по дате рождения.

    Учитывает, что китайский Новый год наступает в конце января —
    середине февраля, поэтому для дат до ~20 февраля берётся
    предыдущий год.
    """
    year = bday.year
    if (bday.month, bday.day) < (2, 20):
        year -= 1
    return EASTERN_ANIMALS[(year - 4) % 12]


# ---------- Нумерология ----------

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
    """Складывает цифры числа, пока не получится одна цифра (1–9)."""
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def life_path_number(bday):
    """Число жизненного пути по дате рождения (1–9)."""
    return digit_sum(bday.day + bday.month + bday.year)


def personal_day_number(bday):
    """Персональное число дня: life path + сегодняшняя дата."""
    today = datetime.date.today()
    return digit_sum(life_path_number(bday) + today.day + today.month)


# ---------- Жизнь в разных единицах ----------

def life_in_units(bday):
    """Возвращает словарь с прожитым временем в разных единицах."""
    days = (datetime.date.today() - bday).days

    return {
        "days":       days,
        "hours":      days * 24,
        "minutes":    days * 24 * 60,
        "seconds":    days * 24 * 60 * 60,
        "heartbeats": days * 24 * 60 * 70,     # ~70 уд/мин
        "breaths":    days * 24 * 60 * 16,     # ~16 вдохов/мин
        "sleep_days": days // 3,               # ~треть жизни во сне
    }


def format_big_number(n):
    """Форматирует число с пробелами как разделителями тысяч."""
    return f"{n:,}".replace(",", " ")
    
# ---------- Совместимость имён ----------

COMPATIBILITY_VERDICTS = [
    (85, "💞 Идеальная пара! Вам суждено быть вместе."),
    (70, "💖 Отличная совместимость. Доверяйте друг другу."),
    (55, "💛 Хорошие шансы. Работайте над отношениями."),
    (40, "💙 Есть над чем поработать, но всё возможно."),
    (25, "💚 Дружба — тоже прекрасно!"),
    (0,  "💔 Звёзды советуют остаться друзьями."),
]


def name_compatibility(name1, name2):
    """Возвращает (процент, вердикт) для двух имён."""
    a, b = sorted([name1.lower().strip(), name2.lower().strip()])
    seed = f"{a}+{b}"
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    percent = h % 101  # 0..100

    for threshold, verdict in COMPATIBILITY_VERDICTS:
        if percent >= threshold:
            return percent, verdict
    return percent, COMPATIBILITY_VERDICTS[-1][1]    
    
# ---------- Поколение ----------

GENERATIONS = [
    (1928, 1945, "🎩 Молчаливое поколение"),
    (1946, 1964, "👔 Бэби-бумеры"),
    (1965, 1980, "🎸 Поколение X"),
    (1981, 1996, "💾 Поколение Y (миллениалы)"),
    (1997, 2012, "📱 Поколение Z (зумеры)"),
    (2013, 2100, "🚀 Поколение Альфа"),
]


def generation(bday):
    """Возвращает название поколения по году рождения."""
    year = bday.year
    for start, end, name in GENERATIONS:
        if start <= year <= end:
            return name
    return "🌍 Неизвестное поколение"   
    
# ---------- Место рождения ----------

CITY_VIBES = [
    "🌊 город мечтателей и романтиков",
    "🏔️ город сильных духом",
    "🔥 город страсти и движения",
    "🌿 город спокойствия и мудрости",
    "⚡ город скорости и перемен",
    "🎭 город тайн и вдохновения",
    "🌟 город удачи и возможностей",
    "📚 город знаний и традиций",
]

CITY_ELEMENTS = [
    ("🔥 Огонь", "Энергия, страсть, лидерство"),
    ("💧 Вода",  "Гибкость, интуиция, глубина"),
    ("🌪️ Воздух","Свобода, общение, идеи"),
    ("🌍 Земля", "Надёжность, терпение, стабильность"),
]

CITY_SACRED_NUMBERS = {
    1: "символ начала и лидерства",
    2: "символ партнёрства и гармонии",
    3: "символ творчества и радости",
    4: "символ порядка и стабильности",
    5: "символ перемен и свободы",
    6: "символ заботы и семьи",
    7: "символ тайны и мудрости",
    8: "символ силы и достижений",
    9: "символ завершения и служения",
}


def birth_place_horoscope(city):
    """Возвращает 'астрологический портрет' родного города."""
    city_clean = city.strip().lower()
    h = int(hashlib.md5(city_clean.encode()).hexdigest(), 16)

    letters = len([c for c in city if c.isalpha()])
    sacred = letters % 9 or 9

    return {
        "city":           city.strip(),
        "letters":        letters,
        "vibe":           CITY_VIBES[h % len(CITY_VIBES)],
        "element":        CITY_ELEMENTS[(h // 7) % len(CITY_ELEMENTS)],
        "sacred":         sacred,
        "sacred_meaning": CITY_SACRED_NUMBERS[sacred],
    }    


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
    """Возвращает приветствие в выбранном стиле (с цветом)."""
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
    print(f"{Color.YELLOW}🌟 Предсказание на сегодня: "
          f"{daily_prediction(name)}{Color.RESET}")

    print()
    print(f"{Color.CYAN}📊 Ваши биоритмы на сегодня:{Color.RESET}")
    bio = biorhythm(bday)
    print(f"  Физический:      {render_bar(bio['physical'])}  "
          f"{bio['physical']:+.2f}")
    print(f"  Эмоциональный:   {render_bar(bio['emotional'])}  "
          f"{bio['emotional']:+.2f}")
    print(f"  Интеллектуальный:{render_bar(bio['intellectual'])}  "
          f"{bio['intellectual']:+.2f}")

    print()
    print(f"{Color.PURPLE}🚀 Ваш возраст на других планетах:{Color.RESET}")
    for planet, age in cosmic_age(bday):
        print(f"  {planet:<12} {age:>7.2f} лет")

    print()
    print(f"{Color.RED}🐲 Восточный календарь: "
          f"{eastern_animal(bday)}{Color.RESET}")

    print()
    life_path = life_path_number(bday)
    day_num = personal_day_number(bday)
    print(f"{Color.CYAN}🔢 Число жизненного пути: {life_path}{Color.RESET}")
    print(f"   {LIFE_PATH_MEANINGS[life_path]}")
    print(f"{Color.CYAN}📅 Персональное число дня: {day_num}{Color.RESET}")

    print()
    print(f"{Color.BLUE}⏳ Ваша жизнь в разных единицах:{Color.RESET}")
    units = life_in_units(bday)
    print(f"  Дней:          {format_big_number(units['days'])}")
    print(f"  Часов:         {format_big_number(units['hours'])}")
    print(f"  Минут:         {format_big_number(units['minutes'])}")
    print(f"  Секунд:        {format_big_number(units['seconds'])}")
    print(f"  Ударов сердца: {format_big_number(units['heartbeats'])}")
    print(f"  Вдохов:        {format_big_number(units['breaths'])}")
    print(f"  Дней во сне:   {format_big_number(units['sleep_days'])}")
    
    print()
    print(f"{Color.PURPLE}💘 Проверка совместимости имён:{Color.RESET}")
    other = input("  Введите имя второй половинки (или Enter, чтобы пропустить): ").strip()
    if other:
        percent, verdict = name_compatibility(name, other)
        bar_len = 20
        filled = int(percent / 100 * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"  {name} ❤ {other}")
        print(f"  {bar}  {percent}%")
        print(f"  {verdict}")
    else:
        print("  Пропущено.")
        
    print()
    print(f"{Color.YELLOW}👥 Ваше поколение: "
          f"{generation(bday)}{Color.RESET}")    
          
    print()
    print(f"{Color.GREEN}🏡 Магия места рождения:{Color.RESET}")
    city = input("  В каком городе вы родились? ").strip()
    if city:
        horo = birth_place_horoscope(city)
        print(f"  🌆 {horo['city']}")
        print(f"  Характер: {horo['vibe']}")
        print(f"  Стихия:   {horo['element'][0]} — {horo['element'][1]}")
        print(f"  Сакральное число: {horo['sacred']} "
              f"— {horo['sacred_meaning']}")
    else:
        print("  Пропущено.")      

    print()
    if info["days_to_next"] == 0:
        print(f"{Color.BOLD}{Color.RED}🎉 С днём рождения! 🎉{Color.RESET}")
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
