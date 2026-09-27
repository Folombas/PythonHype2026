#!/usr/bin/env python3
"""HelloPythonGUI.py — графическая версия HelloPython на Tkinter.

Запуск:  python3 HelloPythonGUI.py  (из папки HelloPython)
"""

import datetime
import re
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from hellopython.dates import parse_date
from hellopython.age import age_info
from hellopython.utils import plural_years, plural_days, format_big_number
from hellopython.prediction import daily_prediction
from hellopython.biorhythm import biorhythm, render_bar
from hellopython.cosmos import cosmic_age
from hellopython.eastern import eastern_animal
from hellopython.numerology import (
    life_path_number, personal_day_number, LIFE_PATH_MEANINGS,
)
from hellopython.units import life_in_units
from hellopython.compatibility import name_compatibility
from hellopython.generation import generation
from hellopython.birthplace import birth_place_horoscope
from hellopython.profile import build_profile_text, save_profile
from hellopython.moon import moon_report


THEMES = {
    "dark": {
        "bg":          "#1e1e1e",
        "fg":          "#d4d4d4",
        "insert":      "#d4d4d4",
        "select_bg":   "#264f78",
        "header":      "#4ec9b0",
        "accent":      "#dcdcaa",
        "value":       "#ce9178",
        "good":        "#b5cea8",
        "error":       "#f48771",
    },
    "light": {
        "bg":          "#ffffff",
        "fg":          "#1e1e1e",
        "insert":      "#1e1e1e",
        "select_bg":   "#cce5ff",
        "header":      "#0f6b5c",
        "accent":      "#7a5c00",
        "value":       "#a31515",
        "good":        "#2e7d32",
        "error":       "#c62828",
    },
}


def _strip_ansi(s):
    return re.sub(r'\x1b\[[0-9;]*m', '', s)


class HelloPythonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HelloPython — персональный расчёт")
        self.root.geometry("920x720")
        self.root.minsize(700, 500)

        self.name_var    = tk.StringVar()
        self.bday_var    = tk.StringVar()
        self.city_var    = tk.StringVar()
        self.partner_var = tk.StringVar()
        self.theme_var   = tk.StringVar(value="dark")

        self.last_data = None
        self.theme = THEMES["dark"]

        self._build_ui()
        self._apply_theme()

    def _build_ui(self):
        top = ttk.LabelFrame(self.root, text="Исходные данные", padding=10)
        top.pack(fill="x", padx=10, pady=(10, 5))

        ttk.Label(top, text="Имя:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
        ttk.Entry(top, textvariable=self.name_var, width=28).grid(row=0, column=1, sticky="w", padx=5, pady=3)

        ttk.Label(top, text="Дата рождения (ДД.ММ.ГГГГ):").grid(row=0, column=2, sticky="e", padx=5, pady=3)
        ttk.Entry(top, textvariable=self.bday_var, width=16).grid(row=0, column=3, sticky="w", padx=5, pady=3)

        ttk.Label(top, text="Родной город:").grid(row=1, column=0, sticky="e", padx=5, pady=3)
        ttk.Entry(top, textvariable=self.city_var, width=28).grid(row=1, column=1, sticky="w", padx=5, pady=3)

        ttk.Label(top, text="Имя второй половинки:").grid(row=1, column=2, sticky="e", padx=5, pady=3)
        ttk.Entry(top, textvariable=self.partner_var, width=16).grid(row=1, column=3, sticky="w", padx=5, pady=3)

        btns = ttk.Frame(self.root)
        btns.pack(fill="x", padx=10, pady=5)

        ttk.Button(btns, text="Рассчитать", command=self.calculate).pack(side="left", padx=3)
        ttk.Button(btns, text="Сохранить профиль", command=self.save).pack(side="left", padx=3)
        ttk.Button(btns, text="Очистить", command=self.clear).pack(side="left", padx=3)
        ttk.Button(btns, text="Выход", command=self.root.destroy).pack(side="right", padx=3)

        ttk.Label(btns, text="Тема:").pack(side="right", padx=(20, 3))
        theme_cb = ttk.Combobox(
            btns, textvariable=self.theme_var,
            values=["dark", "light"], state="readonly", width=8,
        )
        theme_cb.pack(side="right", padx=3)
        theme_cb.bind("<<ComboboxSelected>>", lambda e: self._apply_theme())

        self.text = scrolledtext.ScrolledText(
            self.root, wrap="word", font=("Monospace", 10),
            relief="flat", borderwidth=0,
        )
        self.text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.text.configure(state="disabled")

    def _apply_theme(self):
        name = self.theme_var.get()
        self.theme = THEMES.get(name, THEMES["dark"])
        c = self.theme

        self.text.configure(
            bg=c["bg"], fg=c["fg"], insertbackground=c["insert"],
            selectbackground=c["select_bg"],
        )
        self.text.tag_configure("header", foreground=c["header"],
                                font=("Monospace", 11, "bold"))
        self.text.tag_configure("accent", foreground=c["accent"])
        self.text.tag_configure("value",  foreground=c["value"])
        self.text.tag_configure("good",   foreground=c["good"])
        self.text.tag_configure("error",  foreground=c["error"])

    def calculate(self):
        name = self.name_var.get().strip() or "друг"
        raw_date = self.bday_var.get().strip()
        city = self.city_var.get().strip()
        partner = self.partner_var.get().strip()

        bday = parse_date(raw_date)
        if bday is None:
            self._show_error("Неверный формат даты. Пример: 30.11.1987")
            return
        if bday > datetime.date.today():
            self._show_error("Дата рождения не может быть в будущем.")
            return

        info = age_info(bday)
        bio = biorhythm(bday)
        units = life_in_units(bday)
        life_path = life_path_number(bday)
        day_num = personal_day_number(bday)
        gen = generation(bday)
        eastern = eastern_animal(bday)
        prediction = _strip_ansi(daily_prediction(name))
        cosmic = cosmic_age(bday)
        moon = moon_report(bday)

        city_horo = birth_place_horoscope(city) if city else None

        compat = None
        if partner:
            pct, verdict = name_compatibility(name, partner)
            compat = {"other": partner, "percent": pct, "verdict": verdict}

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
            "bio": bio,
            "cosmic": cosmic,
        }

        self.last_data = (name, bday, info, extras)
        self._render(name, bday, info, extras)

    def _render(self, name, bday, info, extras):
        t = self.text
        t.configure(state="normal")
        t.delete("1.0", "end")

        def w(line="", tag=None):
            t.insert("end", line + "\n", tag or "")

        w("=" * 60, "header")
        w(f"   {name}", "header")
        w(f"   Отчёт от {datetime.datetime.now():%d.%m.%Y %H:%M}", "header")
        w("=" * 60, "header")
        w()

        w(f"Дата рождения: {bday:%d.%m.%Y}  ({info['weekday']})")
        w(f"Возраст: {info['years']} {plural_years(info['years'])}")
        w(f"Знак зодиака: {info['zodiac']}", "accent")
        w()

        w("Предсказание на сегодня:", "header")
        w(f"   {extras['prediction']}", "value")
        w()

        w("Биоритмы:", "header")
        b = extras["bio"]
        for label, key in (("Физический:      ", "physical"),
                           ("Эмоциональный:   ", "emotional"),
                           ("Интеллектуальный:", "intellectual")):
            v = b[key]
            w(f"   {label} {render_bar(v)}  {v:+.2f}", "value")
        w()

        w("Возраст на других планетах:", "header")
        for planet, age in extras["cosmic"]:
            w(f"   {planet:<12} {age:>7.2f} лет", "value")
        w()

        w(f"Восточный календарь: {extras['eastern']}", "accent")
        w()

        w(f"Число жизненного пути: {extras['life_path']}", "header")
        w(f"   {LIFE_PATH_MEANINGS[extras['life_path']]}", "value")
        w(f"Персональное число дня: {extras['day_num']}", "header")
        w()

        w("Жизнь в разных единицах:", "header")
        u = extras["units"]
        for key, label in (
            ("days",       "Дней:          "),
            ("hours",      "Часов:         "),
            ("minutes",    "Минут:         "),
            ("seconds",    "Секунд:        "),
            ("heartbeats", "Ударов сердца: "),
            ("breaths",    "Вдохов:        "),
            ("sleep_days", "Дней во сне:   "),
        ):
            w(f"   {label}{format_big_number(u[key])}", "value")
        w()

        if extras.get("compatibility"):
            c = extras["compatibility"]
            w("Совместимость имён:", "header")
            filled = int(c["percent"] / 100 * 20)
            bar = "█" * filled + "░" * (20 - filled)
            w(f"   {name} ❤ {c['other']}", "value")
            w(f"   {bar}  {c['percent']}%", "value")
            w(f"   {c['verdict']}", "value")
            w()

        w(f"Поколение: {extras['generation']}", "accent")
        w()

        if extras.get("city_horo"):
            h = extras["city_horo"]
            w("Магия места рождения:", "header")
            w(f"   {h['city']}", "value")
            w(f"   Характер: {h['vibe']}", "value")
            w(f"   Стихия:   {h['element'][0]} — {h['element'][1]}", "value")
            w(f"   Сакральное число: {h['sacred']} — "
              f"{h['sacred_meaning']}", "value")
            w()

        m = extras["moon"]
        w("Лунная фаза:", "header")
        w(f"   При рождении: {m['bday_name']} "
          f"(освещённость {m['bday_illumination']:.0f}%)", "value")
        w(f"   Сегодня:      {m['today_name']} "
          f"(освещённость {m['today_illumination']:.0f}%)", "value")
        w()

        if info["days_to_next"] == 0:
            w("С ДНЁМ РОЖДЕНИЯ!", "good")
        else:
            w(f"До следующего дня рождения: {info['days_to_next']} "
              f"{plural_days(info['days_to_next'])}.", "accent")

        t.configure(state="disabled")

    def save(self):
        if self.last_data is None:
            messagebox.showwarning("Нет данных",
                                   "Сначала нажмите «Рассчитать».")
            return
        name, bday, info, extras = self.last_data
        extras_for_save = {k: v for k, v in extras.items()
                           if k not in ("bio", "cosmic")}
        try:
            text = build_profile_text(name, bday, info, extras_for_save)
            path = save_profile(name, text)
            messagebox.showinfo("Готово", f"Профиль сохранён:\n{path}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def clear(self):
        self.name_var.set("")
        self.bday_var.set("")
        self.city_var.set("")
        self.partner_var.set("")
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")
        self.last_data = None

    def _show_error(self, msg):
        t = self.text
        t.configure(state="normal")
        t.delete("1.0", "end")
        t.insert("end", msg + "\n", "error")
        t.configure(state="disabled")


def main():
    root = tk.Tk()
    HelloPythonApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
