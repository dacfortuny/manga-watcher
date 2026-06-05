from unittest.mock import Mock, patch

import pytest
import requests

from src.scrapping import extract_watch_entries, fetch_calendar_lines


def test_extract_watch_entries_basic():
    lines = ["Lunes, 8 Enero 2026", "- One Piece vol 120"]
    result = extract_watch_entries(lines, ["One Piece"])
    assert result == {"One Piece": [["Lunes, 8 Enero 2026", "- One Piece vol 120"]]}


def test_extract_watch_entries_case_insensitive():
    lines = ["Lunes, 8 Enero 2026", "- ONE PIECE vol 120"]
    result = extract_watch_entries(lines, ["One Piece"])
    assert result == {"One Piece": [["Lunes, 8 Enero 2026", "- ONE PIECE vol 120"]]}


def test_extract_watch_entries_longest_match_wins():
    lines = ["Lunes, 8 Enero 2026", "- Dragon Ball Super vol 5"]
    result = extract_watch_entries(lines, ["Dragon Ball", "Dragon Ball Super"])
    assert result["Dragon Ball Super"] == [["Lunes, 8 Enero 2026", "- Dragon Ball Super vol 5"]]
    assert result["Dragon Ball"] == []


def test_extract_watch_entries_no_match():
    lines = ["Lunes, 8 Enero 2026", "- Naruto vol 1"]
    result = extract_watch_entries(lines, ["One Piece"])
    assert result == {"One Piece": []}


def test_extract_watch_entries_item_before_date_is_skipped():
    lines = ["- One Piece vol 120", "Lunes, 8 Enero 2026", "- One Piece vol 121"]
    result = extract_watch_entries(lines, ["One Piece"])
    assert result == {"One Piece": [["Lunes, 8 Enero 2026", "- One Piece vol 121"]]}


def test_extract_watch_entries_multiple_dates():
    lines = [
        "Lunes, 8 Enero 2026",
        "- One Piece vol 120",
        "Martes, 9 Enero 2026",
        "- One Piece vol 121",
    ]
    result = extract_watch_entries(lines, ["One Piece"])
    assert len(result["One Piece"]) == 2


def test_extract_watch_entries_empty_watch_list():
    lines = ["Lunes, 8 Enero 2026", "- One Piece vol 120"]
    result = extract_watch_entries(lines, [])
    assert result == {}


def _mock_response(html: str) -> Mock:
    resp = Mock()
    resp.text = html
    resp.raise_for_status = Mock()
    return resp


def test_fetch_calendar_lines_buffers_multiline_item():
    # "-" alone starts a buffer; following non-date line continues it
    html = "<html><body>Lunes, 8 Enero 2026\n-\nOne Piece vol 120\nMartes, 9 Enero 2026</body></html>"
    with patch("src.scrapping.requests.get", return_value=_mock_response(html)):
        lines = fetch_calendar_lines("http://example.com")
    assert "- One Piece vol 120" in lines
    assert "Lunes, 8 Enero 2026" in lines
    assert "Martes, 9 Enero 2026" in lines


def test_fetch_calendar_lines_flushes_trailing_buffer():
    html = "<html><body>Lunes, 8 Enero 2026\n-\nOne Piece vol 120</body></html>"
    with patch("src.scrapping.requests.get", return_value=_mock_response(html)):
        lines = fetch_calendar_lines("http://example.com")
    assert "- One Piece vol 120" in lines


def test_fetch_calendar_lines_skips_empty_lines():
    html = "<html><body>Lunes, 8 Enero 2026\n\n\n-\nOne Piece vol 120</body></html>"
    with patch("src.scrapping.requests.get", return_value=_mock_response(html)):
        lines = fetch_calendar_lines("http://example.com")
    assert "" not in lines


def test_fetch_calendar_lines_raises_on_http_error():
    resp = Mock()
    resp.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
    with patch("src.scrapping.requests.get", return_value=resp):
        with pytest.raises(requests.HTTPError):
            fetch_calendar_lines("http://example.com")
