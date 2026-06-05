from checker import compute_changes

FUTURE_DATE = "Lunes, 1 Enero 2099"
PAST_DATE = "Lunes, 1 Enero 2020"


def test_compute_changes_no_changes():
    state = {"One Piece": [[FUTURE_DATE, "- One Piece vol 1"]]}
    changes = compute_changes(state, state)
    assert changes == {"entries_added": [], "entries_removed": []}


def test_compute_changes_added():
    old = {"One Piece": []}
    new = {"One Piece": [[FUTURE_DATE, "- One Piece vol 1"]]}
    changes = compute_changes(old, new)
    assert any("One Piece" in s for s in changes["entries_added"])
    assert changes["entries_removed"] == []


def test_compute_changes_removed_future():
    old = {"One Piece": [[FUTURE_DATE, "- One Piece vol 1"]]}
    new = {"One Piece": []}
    changes = compute_changes(old, new)
    assert changes["entries_added"] == []
    assert any("One Piece" in s for s in changes["entries_removed"])


def test_compute_changes_removed_past_not_reported():
    old = {"One Piece": [[PAST_DATE, "- One Piece vol 1"]]}
    new = {"One Piece": []}
    changes = compute_changes(old, new)
    assert changes == {"entries_added": [], "entries_removed": []}


def test_compute_changes_date_header_in_added():
    old = {"One Piece": []}
    new = {"One Piece": [[FUTURE_DATE, "- One Piece vol 1"]]}
    changes = compute_changes(old, new)
    assert FUTURE_DATE in changes["entries_added"][0]


def test_compute_changes_date_header_in_removed():
    old = {"One Piece": [[FUTURE_DATE, "- One Piece vol 1"]]}
    new = {"One Piece": []}
    changes = compute_changes(old, new)
    assert FUTURE_DATE in changes["entries_removed"][0]


def test_compute_changes_sorted_by_date():
    date1 = "Lunes, 1 Enero 2099"
    date2 = "Martes, 2 Enero 2099"
    old = {"One Piece": []}
    new = {"One Piece": [[date2, "- One Piece B"], [date1, "- One Piece A"]]}
    changes = compute_changes(old, new)
    added = changes["entries_added"]
    pos1 = next(i for i, s in enumerate(added) if date1 in s)
    pos2 = next(i for i, s in enumerate(added) if date2 in s)
    assert pos1 < pos2


def test_compute_changes_title_absent_in_old():
    old = {}
    new = {"One Piece": [[FUTURE_DATE, "- One Piece vol 1"]]}
    changes = compute_changes(old, new)
    assert any("One Piece" in s for s in changes["entries_added"])


def test_compute_changes_multiple_titles():
    old = {"One Piece": [], "Naruto": []}
    new = {
        "One Piece": [[FUTURE_DATE, "- One Piece vol 1"]],
        "Naruto": [[FUTURE_DATE, "- Naruto vol 1"]],
    }
    changes = compute_changes(old, new)
    added_text = " ".join(changes["entries_added"])
    assert "One Piece" in added_text
    assert "Naruto" in added_text
