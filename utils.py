from datetime import date, datetime


def pars_datetoken(token: str):
    token = token.lower().strip()
    if token == "today":
        return date.today().isoformat()
    try:
        dt = datetime.fromisoformat(token)
        return dt.date().isoformat()
    except:
        return None


def days_until(last_iso: str, interval: int):
    last = datetime.fromisoformat(last_iso).date()
    difference = (date.today() - last).days
    return interval - difference
