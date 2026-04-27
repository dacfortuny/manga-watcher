from datetime import date

from src.dates import calendar_url_for, month_year_iter, parse_spanish_date
from src.email import send_email
from src.files import load_state, load_watch_list, merge_states, save_state
from src.scrapping import extract_watch_entries, fetch_calendar_lines


def compute_changes(old: dict, new: dict) -> list[str]:
    """Compute the changes between the old and new state.
    Args:
        old (dict): The old state of the calendar.
        new (dict): The new state of the calendar.
    Returns:
        dict[str, list[str]]: A dictionary with lists of added and removed entries.
    """

    entries_added = []
    entries_removed = []

    added = set()
    removed = set()
    for title in new:
        old_set = set(tuple(x) for x in old.get(title, []))
        new_set = set(tuple(x) for x in new.get(title, []))

        added = added.union(new_set - old_set)
        removed = removed.union(old_set - new_set)

    added_dt = [(parse_spanish_date(date_str), date_str, item) for date_str, item in added]
    added_dt.sort(key=lambda x: (x[0], x[2]))
    
    removed_dt = [(parse_spanish_date(date_str), date_str, item) for date_str, item in removed]
    removed_dt.sort(key=lambda x: (x[0], x[2]))

    date_str_prev = ""
    for _, date_str, item in added_dt:
        if date_str != date_str_prev:
            entries_added.append((
                date_str,
                f"\n{date_str}"
            ))
        entries_added.append((
            date_str,
            f"{item}"
        ))
        date_str_prev = date_str

    date_str_prev = ""
    for _, date_str, item in removed_dt:
        if date_str != date_str_prev:
            entries_removed.append((
                date_str,
                f"\n{date_str}"
            ))
        entries_removed.append((
            date_str,
            f"{item}"
        ))
        date_str_prev = date_str

    # Return only the formatted messages
    return {"entries_added": [msg for _, msg in entries_added],
            "entries_removed": [msg for _, msg in entries_removed]}


def main():
    watch = load_watch_list()

    new_state = {w: [] for w in watch}

    start = date.today()
    checked_urls = []

    for month, year in month_year_iter(start, months_ahead=12):
        url = calendar_url_for(month, year)
        checked_urls.append(url)

        try:
            lines = fetch_calendar_lines(url)
        except Exception as e:
            print(f"Warning: failed to fetch {url}: {e}")
            continue

        month_state = extract_watch_entries(lines, watch)
        new_state = merge_states(new_state, month_state)

    old_state = load_state()
    changes = compute_changes(old_state, new_state)

    if changes["entries_added"] or changes["entries_removed"]:
        try:
            send_email(changes)
        except Exception as e:
            print(f"Warning: failed to send email: {e}")

    save_state(new_state)


if __name__ == "__main__":
    main()
