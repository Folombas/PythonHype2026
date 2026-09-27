"""Космический возраст."""
import datetime

PLANETS = [
    ("☿ Меркурий", 0.2408467), ("♀ Венера", 0.61519726),
    ("♂ Марс", 1.8808158), ("♃ Юпитер", 11.862615),
    ("♄ Сатурн", 29.447498), ("⛢ Уран", 84.016846),
    ("♆ Нептун", 164.79132),
]

def cosmic_age(bday):
    earth_years = (datetime.date.today() - bday).days / 365.2425
    return [(name, earth_years / period) for name, period in PLANETS]
