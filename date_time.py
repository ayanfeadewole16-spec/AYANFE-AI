# ============================================
# AYANFE AI V2 — DATE & TIME SYSTEM
# ============================================

from datetime import datetime
from zoneinfo import ZoneInfo


DEFAULT_TIMEZONE = "Africa/Lagos"


def get_current_datetime(timezone_name=DEFAULT_TIMEZONE):
    """
    Get the current date and time in a specified timezone.
    Default is Nigeria time (Africa/Lagos), not UTC.
    """

    try:
        tz = ZoneInfo(timezone_name)
    except Exception:
        tz = ZoneInfo(DEFAULT_TIMEZONE)

    now = datetime.now(tz)

    return {
        "date": now.strftime("%Y-%m-%d"),
        "formatted_date": now.strftime("%A, %B %d, %Y"),
        "time": now.strftime("%I:%M %p"),
        "day": now.strftime("%A"),
        "timezone": timezone_name,
        "iso": now.isoformat()
    }


def get_local_datetime():
    """
    Get AYANFE's default local time.
    """

    return get_current_datetime(DEFAULT_TIMEZONE)


def get_date_context():
    """
    Context for AYANFE's brain.
    """

    current = get_local_datetime()

    return (
        f"Current date: {current['formatted_date']}. "
        f"Current time: {current['time']}. "
        f"Timezone: {current['timezone']}."
    )


def get_time_in_timezone(timezone_name):
    """
    Get the current time in another location.

    Example:
        Europe/London
        America/New_York
        Africa/Lagos
    """

    current = get_current_datetime(timezone_name)

    return (
        f"The current time in {timezone_name} is "
        f"{current['time']} on {current['formatted_date']}."
    )
