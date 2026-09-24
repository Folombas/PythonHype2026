# HelloPython.py — интерактивное приветствие с меню
# Демонстрирует: input, print, f-строки, функции,
# цикл while, ветвление if/elif/else, словарь, выход через break

import datetime  # стандартный модуль — работает с датой и временем


def greet(name, style):
    """Возвращает приветствие в выбранном стиле."""
    styles = {
        "1": f"Привет, {name}! Добро пожаловать в Python.",
        "2": f"Здравствуйте, {name}. Рады видеть вас снова.",
        "3": f"Хай, {name}! 🐍 Python ждёт тебя.",
        "4": f"Салют, {name}! Сегодня {datetime.date.today():%d.%m.%Y}.",
    }
    return styles.get(style, f"Привет, {name}!")


def main():
    print("=" * 40)
    print("   Программа HelloPython")
    print("=" * 40)

    name = input("Как вас зовут? ").strip()
    if not name:
        name = "друг"

    while True:
        print()
        print("Выберите стиль приветствия:")
        print("  1 — дружеский")
        print("  2 — официальный")
        print("  3 — неформальный")
        print("  4 — с датой")
        print("  0 — выход")

        choice = input("Ваш выбор: ").strip()

        if choice == "0":
            print(f"\nДо встречи, {name}! 👋")
            break
        elif choice in {"1", "2", "3", "4"}:
            print()
            print(greet(name, choice))
        else:
            print("\nНет такого варианта. Попробуйте снова.")


if __name__ == "__main__":
    main()
