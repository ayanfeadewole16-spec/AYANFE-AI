
# ============================================
# AYANFE AI V2 — DATE & TIME
# ============================================

from datetime import datetime, timezone


def get_current_datetime():
    """
    Get the current UTC date/time.
    """

    now = datetime.now(timezone.utc)

    return {
        "date": now.strftime("%Y-%m-%d"),
        "time_utc": now.strftime("%H:%M:%S"),
        "day": now.strftime("%A"),
        "year": now.year,
        "month": now.month,
        "day_number": now.day,
        "iso": now.isoformat()
    }


def get_date_context():
    """
    Return a concise date context for AYANFE's brain.
    """

    current = get_current_datetime()

    return (
        f"Current date: {current['day']}, "
        f"{current['date']}. "
        f"Current UTC time: {current['time_utc']}."
    )
