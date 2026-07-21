from datetime import date
from math import ceil


def age_months(birth_year_month: date, at: date | None = None) -> int:
    at = at or date.today()
    return (at.year - birth_year_month.year) * 12 + at.month - birth_year_month.month


def pages(total: int, size: int) -> int:
    return ceil(total / size) if total else 0


def to_float(value: object | None) -> float | None:
    return None if value is None else float(str(value))
