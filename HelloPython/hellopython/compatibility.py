"""Совместимость имён."""
import hashlib

COMPATIBILITY_VERDICTS = [
    (85, "💞 Идеальная пара! Вам суждено быть вместе."),
    (70, "💖 Отличная совместимость. Доверяйте друг другу."),
    (55, "💛 Хорошие шансы. Работайте над отношениями."),
    (40, "💙 Есть над чем поработать, но всё возможно."),
    (25, "💚 Дружба — тоже прекрасно!"),
    (0,  "💔 Звёзды советуют остаться друзьями."),
]

def name_compatibility(name1, name2):
    a, b = sorted([name1.lower().strip(), name2.lower().strip()])
    seed = f"{a}+{b}"
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    percent = h % 101
    for threshold, verdict in COMPATIBILITY_VERDICTS:
        if percent >= threshold:
            return percent, verdict
    return percent, COMPATIBILITY_VERDICTS[-1][1]
