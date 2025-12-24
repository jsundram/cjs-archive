"""
Date parsing utilities for CSV-to-HTML scripts.

Provides consistent date parsing across all scripts, ensuring that dates
remain stable regardless of when the build script is run.
"""

import dateparser
from datetime import datetime


def format_date_iso(date_str):
    """
    Converts various date formats to YYYY-MM-DD format.

    Uses RELATIVE_BASE to ensure consistent day defaults (1st of month).
    Without this, dateparser uses the current day of the month as default,
    causing parsed dates to vary based on the build date.

    Args:
        date_str: Date string in various formats (M/D/YYYY, MM/YYYY, Mon-YY, etc.)

    Returns:
        str: Date in YYYY-MM-DD format, or original string if parsing fails

    Examples:
        >>> format_date_iso("07/1990")
        "1990-07-01"
        >>> format_date_iso("6/30/2003")
        "2003-06-30"
        >>> format_date_iso("Jul-92")
        "1992-07-01"
    """
    try:
        # Use fixed RELATIVE_BASE to ensure day defaults to 1st of month
        parsed = dateparser.parse(date_str, settings={'RELATIVE_BASE': datetime(2000, 1, 1)})
        if parsed:
            return parsed.strftime('%Y-%m-%d')
        return date_str
    except (ValueError, AttributeError):
        print(f"error parsing: {date_str}")
        return date_str


def format_date_month_year(date_str):
    """
    Converts various date formats to "Month Year" format (e.g., "January 2020").

    Uses RELATIVE_BASE to ensure consistent day defaults (1st of month).

    Args:
        date_str: Date string in various formats (M/D/YYYY, MM/YYYY, etc.)

    Returns:
        str: Date in "Month Year" format, or original string if parsing fails

    Examples:
        >>> format_date_month_year("1/2020")
        "January 2020"
        >>> format_date_month_year("12/15/2019")
        "December 2019"
    """
    try:
        # Use fixed RELATIVE_BASE to ensure day defaults to 1st of month
        parsed = dateparser.parse(date_str, settings={'RELATIVE_BASE': datetime(2000, 1, 1)})
        if parsed:
            return parsed.strftime("%B %Y")
        return date_str
    except (ValueError, AttributeError):
        print(f"error parsing: {date_str}")
        return date_str
