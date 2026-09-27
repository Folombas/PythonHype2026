"""Прожитое время в разных единицах."""
import datetime

def life_in_units(bday):
    days = (datetime.date.today() - bday).days
    return {
        "days":       days,
        "hours":      days * 24,
        "minutes":    days * 24 * 60,
        "seconds":    days * 24 * 60 * 60,
        "heartbeats": days * 24 * 60 * 70,
        "breaths":    days * 24 * 60 * 16,
        "sleep_days": days // 3,
    }
