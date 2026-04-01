import re
from datetime import date

from src.global_variables import BASE_URL

SPANISH_MONTHS = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}

DATE_RE = re.compile(
    r"(Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo),\s+\d+\s+\w+\s+\d{4}",
    re.I
)

def month_year_iter(start: date, months_ahead: int = 12):
    """
    Generate (month, year) tuples starting from 'start' date for 'months_ahead
    months.
    Args:
        start (date): The starting date.
        months_ahead (int): Number of months to generate.
    Yields:
        tuple[int, int]: A tuple of (month, year).
    """
    y, m = start.year, start.month
    for _ in range(months_ahead):
        yield m, y
        m += 1
        if m == 13:
            m = 1
            y += 1

def parse_spanish_date(date_str: str) -> date:
    """
    Parse a Spanish date string of the form 'Lunes, 8 Enero 2026' into a date object.
    Args:
        date_str (str): The Spanish date string.
    Returns:
        date: The corresponding date object.
    """
    # Remove weekday
    _, rest = date_str.split(",", 1)
    rest = rest.strip()  # '8 Enero 2026'

    day_str, month_str, year_str = rest.split()
    day = int(day_str)
    month = SPANISH_MONTHS[month_str.lower()]
    year = int(year_str)

    return date(year, month, day)


def calendar_url_for(month: int, year: int) -> str:
    """
    Generate the calendar URL for a given month and year.
    Args:
        month (int): The month (1-12).
        year (int): The year (e.g., 2026).
    Returns:
        str: The calendar URL.
    """
    return f"{BASE_URL}/calendario.php?mes={month}&ano={year}"