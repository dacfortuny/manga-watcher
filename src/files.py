import json
import os

from src.global_variables import STATE_FILE, WATCH_FILE


def load_watch_list(path: str = WATCH_FILE) -> list[str]:
    """
    Load the watch list from watch file.
    Args:
        path (str): Path to the watch file.
    Returns:
        list[str]: A list of manga titles to watch.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"{path} not found (it must be in the same directory as checker.py)."
        )

    watch: list[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            watch.append(line)

    if not watch:
        raise ValueError("watch.txt is empty (add at least one manga title).")

    return watch


def load_state() -> dict:
    """
    Load the previous execution state from state file.
    Returns:
        dict: The previous state as a dictionary.
    """
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state: dict):
    """
    Save the current execution state to sate file.
    Args:
        state (dict): The state to save.
    """
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def merge_states(total: dict, part: dict) -> dict:
    """
    Merge two states of the form: {title: [[date, item], ...]}
    De-dupes by converting to sets of tuples.
    """
    merged = {}
    all_titles = set(total.keys()) | set(part.keys())
    for t in all_titles:
        a = set(tuple(x) for x in total.get(t, []))
        b = set(tuple(x) for x in part.get(t, []))
        merged[t] = sorted([list(x) for x in (a | b)])
    return merged