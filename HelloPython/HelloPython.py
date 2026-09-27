# HelloPython.py — точка входа.
from hellopython.colors        import Color
from hellopython.dates         import ask_birth_date
from hellopython.age           import age_info
from hellopython.utils         import plural_years, plural_days, format_big_number
from hellopython.prediction    import daily_prediction
from hellopython.biorhythm     import biorhythm, render_bar
from hellopython.cosmos        import cosmic_age
from hellopython.eastern       import eastern_animal
from hellopython.numerology    import (
    life_path_number, personal_day_number, LIFE_PATH_MEANINGS,
)
from hellopython.units         import life_in_units
from hellopython.compatibility import name_compatibility
from hellopython.generation    import generation
from hellopython.birthplace    import birth_place_horoscope
from hellopython.greetings     import greet
from hellopython.profile       import build_profile_text, save_profile
from hellopython.moon          import moon_report


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

    prediction = daily_prediction(name)
    print(f"{Color.YELLOW}🌟 Предсказание на сегодня: "
          f"{prediction}{Color.RESET}")

    print()
    print(f"{Color.CYAN}📊 Ваши биоритмы на сегодня:{Color.RESET}")
    bio = biorhythm(bday)
    for label, key in (("Физический:      ", "physical"),
                       ("Эмоциональный:   ", "emotional"),
                       ("Интеллектуальный:", "intellectual")):
        v = bio[key]
        print(f"  {label} {render_bar(v)}  {v:+.2f}")

    print()
    print(f"{Color.PURPLE}🚀 Ваш возраст на других планетах:{Color.RESET}")
    for planet, age in cosmic_age(bday):
        print(f"  {planet:<12} {age:>7.2f} лет")

    eastern = eastern_animal(bday)
    print()
    print(f"{Color.RED}🐲 Восточный календарь: {eastern}{Color.RESET}")

    life_path = life_path_number(bday)
    day_num = personal_day_number(bday)
    print()
    print(f"{Color.CYAN}🔢 Число жизненного пути: {life_path}{Color.RESET}")
    print(f"   {LIFE_PATH_MEANINGS[life_path]}")
    print(f"{Color.CYAN}📅 Персональное число дня: {day_num}{Color.RESET}")

    units = life_in_units(bday)
    print()
    print(f"{Color.BLUE}⏳ Ваша жизнь в разных единицах:{Color.RESET}")
    print(f"  Дней:          {format_big_number(units['days'])}")
    print(f"  Часов:         {format_big_number(units['hours'])}")
    print(f"  Минут:         {format_big_number(units['minutes'])}")
    print(f"  Секунд:        {format_big_number(units['seconds'])}")
    print(f"  Ударов сердца: {format_big_number(units['heartbeats'])}")
    print(f"  Вдохов:        {format_big_number(units['breaths'])}")
    print(f"  Дней во сне:   {format_big_number(units['sleep_days'])}")

    compat = None
    print()
    print(f"{Color.PURPLE}💘 Проверка совместимости имён:{Color.RESET}")
    other = input("  Введите имя второй половинки "
                  "(или Enter, чтобы пропустить): ").strip()
    if other:
        percent, verdict = name_compatibility(name, other)
        bar_len = 20
        filled = int(percent / 100 * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"  {name} ❤ {other}")
        print(f"  {bar}  {percent}%")
        print(f"  {verdict}")
        compat = {"other": other, "percent": percent, "verdict": verdict}
    else:
        print("  Пропущено.")

    gen = generation(bday)
    print()
    print(f"{Color.YELLOW}👥 Ваше поколение: {gen}{Color.RESET}")

    city_horo = None
    print()
    print(f"{Color.GREEN}🏡 Магия места рождения:{Color.RESET}")
    city = input("  В каком городе вы родились? ").strip()
    if city:
        city_horo = birth_place_horoscope(city)
        print(f"  🌆 {city_horo['city']}")
        print(f"  Характер: {city_horo['vibe']}")
        print(f"  Стихия:   {city_horo['element'][0]} — "
              f"{city_horo['element'][1]}")
        print(f"  Сакральное число: {city_horo['sacred']} "
              f"— {city_horo['sacred_meaning']}")
    else:
        print("  Пропущено.")

    # ---------- Лунная фаза ----------
    moon = moon_report(bday)
    print()
    print(f"{Color.WHITE}🌙 Лунная фаза:{Color.RESET}")
    print(f"  При рождении: {moon['bday_emoji']} {moon['bday_name']} "
          f"(освещённость {moon['bday_illumination']:.0f}%)")
    print(f"  Сегодня:      {moon['today_emoji']} {moon['today_name']} "
          f"(освещённость {moon['today_illumination']:.0f}%)")

    print()
    if info["days_to_next"] == 0:
        print(f"{Color.BOLD}{Color.RED}🎉 С днём рождения! 🎉{Color.RESET}")
    else:
        print(f"До следующего дня рождения: {info['days_to_next']} "
              f"{plural_days(info['days_to_next'])}.")

    print()
    save = input(f"{Color.CYAN}💾 Сохранить профиль в файл? (y/n): "
                 f"{Color.RESET}").strip().lower()
    if save == "y":
        extras = {
            "prediction": prediction,
            "units": units,
            "life_path": life_path,
            "day_num": day_num,
            "generation": gen,
            "eastern": eastern,
            "city_horo": city_horo,
            "compatibility": compat,
            "moon": moon,
        }
        text = build_profile_text(name, bday, info, extras)
        path = save_profile(name, text)
        print(f"  ✅ Профиль сохранён: {path}")

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
