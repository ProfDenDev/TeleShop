from datetime import datetime, date, UTC


def utc_now() -> datetime:
    """
    Текущее время UTC.
    """

    return datetime.now(UTC)

def utc_today() -> date:
    return datetime.now(UTC).date()


def utc_timestamp() -> int:
    return int(
        datetime.now(UTC).timestamp()
    )