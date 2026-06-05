from datetime import date

import pytest

from src.dates import SPANISH_MONTHS, calendar_url_for, month_year_iter, parse_spanish_date


def test_parse_spanish_date_basic():
    assert parse_spanish_date("Lunes, 8 Enero 2026") == date(2026, 1, 8)


def test_parse_spanish_date_case_insensitive():
    assert parse_spanish_date("Lunes, 8 ENERO 2026") == date(2026, 1, 8)
    assert parse_spanish_date("Lunes, 8 enero 2026") == date(2026, 1, 8)


def test_parse_spanish_date_all_months():
    for name, num in SPANISH_MONTHS.items():
        d = parse_spanish_date(f"Lunes, 1 {name.capitalize()} 2026")
        assert d.month == num


def test_parse_spanish_date_invalid_month():
    with pytest.raises(KeyError):
        parse_spanish_date("Lunes, 8 January 2026")


def test_parse_spanish_date_all_weekdays():
    weekdays = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for day in weekdays:
        d = parse_spanish_date(f"{day}, 1 Enero 2026")
        assert d == date(2026, 1, 1)


def test_month_year_iter_basic():
    result = list(month_year_iter(date(2026, 1, 1), months_ahead=3))
    assert result == [(1, 2026), (2, 2026), (3, 2026)]


def test_month_year_iter_year_rollover():
    result = list(month_year_iter(date(2025, 11, 1), months_ahead=4))
    assert result == [(11, 2025), (12, 2025), (1, 2026), (2, 2026)]


def test_month_year_iter_from_december():
    result = list(month_year_iter(date(2025, 12, 1), months_ahead=2))
    assert result == [(12, 2025), (1, 2026)]


def test_month_year_iter_default_count():
    result = list(month_year_iter(date(2026, 1, 1)))
    assert len(result) == 12


def test_month_year_iter_spans_two_years():
    result = list(month_year_iter(date(2025, 7, 1), months_ahead=12))
    years = {y for _, y in result}
    assert years == {2025, 2026}


def test_calendar_url_for_contains_params():
    url = calendar_url_for(3, 2026)
    assert "mes=3" in url
    assert "ano=2026" in url


def test_calendar_url_for_starts_with_https():
    url = calendar_url_for(1, 2026)
    assert url.startswith("https://")
