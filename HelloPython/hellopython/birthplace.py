"""Магия места рождения."""
import hashlib

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
