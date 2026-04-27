import requests
from bs4 import BeautifulSoup

from src.dates import DATE_RE
from src.global_variables import UA


def fetch_calendar_lines(url: str) -> list[str]:
    """Fetch and parse calendar lines from the given URL.
    Args:
        url (str): The URL to fetch the calendar from.
    Returns:
        list[str]: A list of cleaned calendar lines.
    """
    
    r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    raw_lines = [ln.strip() for ln in soup.get_text("\n").splitlines()]

    lines: list[str] = []
    buffer: list[str] = []

    for ln in raw_lines:
        if not ln:
            continue

        # Start of a new calendar item
        if ln == "-" or ln.startswith("- "):
            if buffer:
                lines.append(" ".join(buffer))
                buffer = []
            buffer.append("-")

        # Continuation of the same item
        elif buffer and not DATE_RE.search(ln):
            buffer.append(ln)

        else:
            if buffer:
                lines.append(" ".join(buffer))
                buffer = []
            lines.append(ln)

    if buffer:
        lines.append(" ".join(buffer))

    return lines


def extract_watch_entries(lines: list[str], watch: list[str]) -> dict[str, list[list[str]]]:
    """
    Extract watch entries from calendar lines.
    Args:
        lines (list[str]): The calendar lines.
        watch (list[str]): The list of manga titles to watch.
    Returns:
        dict[str, list[list[str]]]: A dictionary mapping manga titles to their release entries.
    """
    current_date = None
    results = {w: set() for w in watch}

    for ln in lines:

        # Detect date headers
        if DATE_RE.search(ln):
            current_date = ln
            continue

        # Detect items
        item = ln.strip()
        if current_date and item.startswith("-"):
            item_lower = item.strip().lower()
            matches = [w for w in watch if w.strip().lower() in item_lower]
            if matches:
                best = max(matches, key=len)
                results[best].add((current_date, item))

    # Convert sets to sorted lists so they can be serialized as JSON
    return {k: sorted([list(x) for x in v]) for k, v in results.items()}