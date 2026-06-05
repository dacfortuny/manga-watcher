from unittest.mock import patch

import pytest

from src.files import load_state, load_watch_list, merge_states, save_state


def test_load_watch_list_basic(tmp_path):
    f = tmp_path / "watch.txt"
    f.write_text("One Piece\nNaruto\n", encoding="utf-8")
    assert load_watch_list(str(f)) == ["One Piece", "Naruto"]


def test_load_watch_list_strips_comments(tmp_path):
    f = tmp_path / "watch.txt"
    f.write_text("# comment\nOne Piece\n# another\nNaruto\n", encoding="utf-8")
    assert load_watch_list(str(f)) == ["One Piece", "Naruto"]


def test_load_watch_list_strips_whitespace(tmp_path):
    f = tmp_path / "watch.txt"
    f.write_text("  One Piece  \n  Naruto  \n", encoding="utf-8")
    assert load_watch_list(str(f)) == ["One Piece", "Naruto"]


def test_load_watch_list_missing_file():
    with pytest.raises(FileNotFoundError):
        load_watch_list("/nonexistent/path/watch.txt")


def test_load_watch_list_empty_file(tmp_path):
    f = tmp_path / "watch.txt"
    f.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        load_watch_list(str(f))


def test_load_watch_list_comments_only(tmp_path):
    f = tmp_path / "watch.txt"
    f.write_text("# comment\n# another\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_watch_list(str(f))


def test_load_watch_list_unicode(tmp_path):
    f = tmp_path / "watch.txt"
    f.write_text("ドラゴンボール\nOne Piece\n", encoding="utf-8")
    assert load_watch_list(str(f)) == ["ドラゴンボール", "One Piece"]


def test_load_state_missing_file(tmp_path):
    with patch("src.files.STATE_FILE", str(tmp_path / "nonexistent.json")):
        assert load_state() == {}


def test_load_state_valid(tmp_path):
    f = tmp_path / "state.json"
    f.write_text('{"One Piece": [["Lunes, 1 Enero 2026", "- One Piece"]]}', encoding="utf-8")
    with patch("src.files.STATE_FILE", str(f)):
        state = load_state()
    assert state == {"One Piece": [["Lunes, 1 Enero 2026", "- One Piece"]]}


def test_save_load_state_roundtrip(tmp_path):
    state = {"One Piece": [["Lunes, 1 Enero 2026", "- One Piece vol 120"]]}
    f = str(tmp_path / "state.json")
    with patch("src.files.STATE_FILE", f):
        save_state(state)
        loaded = load_state()
    assert loaded == state


def test_save_state_preserves_non_ascii(tmp_path):
    state = {"ドラゴンボール": [["Lunes, 1 Enero 2026", "- ドラゴンボール vol 42"]]}
    f = str(tmp_path / "state.json")
    with patch("src.files.STATE_FILE", f):
        save_state(state)
        loaded = load_state()
    assert loaded == state


def test_merge_states_disjoint_titles():
    a = {"One Piece": [["date1", "item1"]]}
    b = {"Naruto": [["date2", "item2"]]}
    merged = merge_states(a, b)
    assert merged["One Piece"] == [["date1", "item1"]]
    assert merged["Naruto"] == [["date2", "item2"]]


def test_merge_states_deduplication():
    entry = ["date1", "item1"]
    a = {"One Piece": [entry]}
    b = {"One Piece": [entry]}
    merged = merge_states(a, b)
    assert merged["One Piece"] == [entry]


def test_merge_states_combines_entries():
    a = {"One Piece": [["date1", "item1"]]}
    b = {"One Piece": [["date2", "item2"]]}
    merged = merge_states(a, b)
    assert len(merged["One Piece"]) == 2


def test_merge_states_empty_both():
    assert merge_states({}, {}) == {}


def test_merge_states_empty_part():
    a = {"One Piece": [["date1", "item1"]]}
    merged = merge_states(a, {})
    assert merged["One Piece"] == [["date1", "item1"]]


def test_merge_states_empty_total():
    b = {"One Piece": [["date1", "item1"]]}
    merged = merge_states({}, b)
    assert merged["One Piece"] == [["date1", "item1"]]
