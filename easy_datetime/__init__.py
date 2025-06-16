"""
Easy DateTime - A comprehensive datetime utility package.

This package provides easy-to-use functions for datetime manipulation,
conversion, and formatting.
"""

from dateutil import parser
from dateutil.relativedelta import relativedelta
import time
from datetime import datetime, timezone, timedelta
from typing import Union, Optional, List, Dict, Any
import re

__version__ = "1.0.0"
__author__ = "Lucy"
__email__ = "lucy@example.com"

# Export main functions
__all__ = [
    "to_unix",
    "from_unix", 
    "format_datetime",
    "add_time",
    "subtract_time",
    "compare_dates",
    "get_timezone_info",
    "parse_datetime",
    "is_valid_datetime",
    "get_current_unix",
    "get_current_datetime",
    "convert_timezone",
    "get_date_range",
    "calculate_age",
    "get_weekday",
    "is_weekend",
    "get_quarter",
    "round_datetime"
]


def to_unix(datetime_str: str, timezone_str: Optional[str] = None) -> int:
    """
    Convert any datetime string to Unix timestamp.
    
    Args:
        datetime_str (str): A string representing a date/time in any common format
        timezone_str (str, optional): Timezone string (e.g., 'UTC', 'US/Eastern')
        
    Returns:
        int: Unix timestamp (seconds since epoch)
        
    Examples:
        >>> to_unix("2021-01-01")
        1609459200
        >>> to_unix("2021/01/01")
        1609459200
        >>> to_unix("01-01-2021")
        1609459200
        >>> to_unix("2021-01-01 12:00:00", "US/Eastern")
        1609516800
    """
    try:
        parsed_date = parser.parse(datetime_str)
        
        # Handle timezone
        if timezone_str:
            import pytz
            tz = pytz.timezone(timezone_str)
            if parsed_date.tzinfo is None:
                parsed_date = tz.localize(parsed_date)
            else:
                parsed_date = parsed_date.astimezone(tz)
        elif parsed_date.tzinfo is None:
            # If no timezone info, assume UTC
            parsed_date = parsed_date.replace(tzinfo=timezone.utc)
            
        return int(parsed_date.timestamp())
    except (ValueError, TypeError) as e:
        raise ValueError(f"Could not parse datetime string: {datetime_str}") from e


def from_unix(timestamp: Union[int, float], 
              format_str: str = "%Y-%m-%d %H:%M:%S",
              timezone_str: Optional[str] = None) -> str:
    """
    Convert Unix timestamp to formatted datetime string.
    
    Args:
        timestamp (int|float): Unix timestamp
        format_str (str): Output format string (default: "%Y-%m-%d %H:%M:%S")
        timezone_str (str, optional): Target timezone
        
    Returns:
        str: Formatted datetime string
        
    Examples:
        >>> from_unix(1609459200)
        '2021-01-01 00:00:00'
        >>> from_unix(1609459200, "%Y/%m/%d")
        '2021/01/01'
    """
    try:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        
        if timezone_str:
            import pytz
            tz = pytz.timezone(timezone_str)
            dt = dt.astimezone(tz)
            
        return dt.strftime(format_str)
    except (ValueError, TypeError, OSError) as e:
        raise ValueError(f"Could not convert timestamp: {timestamp}") from e


def format_datetime(datetime_str: str, 
                   output_format: str = "%Y-%m-%d %H:%M:%S",
                   input_timezone: Optional[str] = None,
                   output_timezone: Optional[str] = None) -> str:
    """
    Parse and reformat a datetime string.
    
    Args:
        datetime_str (str): Input datetime string
        output_format (str): Desired output format
        input_timezone (str, optional): Input timezone
        output_timezone (str, optional): Output timezone
        
    Returns:
        str: Reformatted datetime string
        
    Examples:
        >>> format_datetime("2021-01-01", "%B %d, %Y")
        'January 01, 2021'
    """
    parsed_date = parser.parse(datetime_str)
    
    # Handle input timezone
    if input_timezone:
        import pytz
        tz = pytz.timezone(input_timezone)
        if parsed_date.tzinfo is None:
            parsed_date = tz.localize(parsed_date)
    elif parsed_date.tzinfo is None:
        parsed_date = parsed_date.replace(tzinfo=timezone.utc)
    
    # Handle output timezone
    if output_timezone:
        import pytz
        tz = pytz.timezone(output_timezone)
        parsed_date = parsed_date.astimezone(tz)
    
    return parsed_date.strftime(output_format)


def add_time(datetime_str: str, 
             years: int = 0, months: int = 0, days: int = 0,
             hours: int = 0, minutes: int = 0, seconds: int = 0) -> str:
    """
    Add time to a datetime string.
    
    Args:
        datetime_str (str): Input datetime string
        years (int): Years to add
        months (int): Months to add
        days (int): Days to add
        hours (int): Hours to add
        minutes (int): Minutes to add
        seconds (int): Seconds to add
        
    Returns:
        str: New datetime string
        
    Examples:
        >>> add_time("2021-01-01", days=30)
        '2021-01-31 00:00:00'
    """
    parsed_date = parser.parse(datetime_str)
    
    # Use relativedelta for years and months, timedelta for the rest
    if years or months:
        parsed_date += relativedelta(years=years, months=months)
    
    if days or hours or minutes or seconds:
        parsed_date += timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    
    return parsed_date.strftime("%Y-%m-%d %H:%M:%S")


def subtract_time(datetime_str: str,
                 years: int = 0, months: int = 0, days: int = 0,
                 hours: int = 0, minutes: int = 0, seconds: int = 0) -> str:
    """
    Subtract time from a datetime string.
    
    Args:
        datetime_str (str): Input datetime string
        years (int): Years to subtract
        months (int): Months to subtract
        days (int): Days to subtract
        hours (int): Hours to subtract
        minutes (int): Minutes to subtract
        seconds (int): Seconds to subtract
        
    Returns:
        str: New datetime string
        
    Examples:
        >>> subtract_time("2021-01-31", days=30)
        '2021-01-01 00:00:00'
    """
    return add_time(datetime_str, -years, -months, -days, -hours, -minutes, -seconds)


def compare_dates(date1: str, date2: str) -> Dict[str, Any]:
    """
    Compare two datetime strings.
    
    Args:
        date1 (str): First datetime string
        date2 (str): Second datetime string
        
    Returns:
        dict: Comparison results including difference and relationship
        
    Examples:
        >>> compare_dates("2021-01-01", "2021-01-02")
        {'difference_days': 1, 'difference_seconds': 86400, 'date1_before_date2': True, ...}
    """
    dt1 = parser.parse(date1)
    dt2 = parser.parse(date2)
    
    # Ensure both have timezone info
    if dt1.tzinfo is None:
        dt1 = dt1.replace(tzinfo=timezone.utc)
    if dt2.tzinfo is None:
        dt2 = dt2.replace(tzinfo=timezone.utc)
    
    diff = dt2 - dt1
    
    return {
        'difference_days': diff.days,
        'difference_seconds': int(diff.total_seconds()),
        'difference_hours': diff.total_seconds() / 3600,
        'difference_minutes': diff.total_seconds() / 60,
        'date1_before_date2': dt1 < dt2,
        'date1_after_date2': dt1 > dt2,
        'dates_equal': dt1 == dt2,
        'absolute_difference_days': abs(diff.days),
        'absolute_difference_seconds': abs(int(diff.total_seconds()))
    }


def get_timezone_info(datetime_str: str) -> Dict[str, Any]:
    """
    Get timezone information from a datetime string.
    
    Args:
        datetime_str (str): Datetime string
        
    Returns:
        dict: Timezone information
    """
    parsed_date = parser.parse(datetime_str)
    
    if parsed_date.tzinfo is None:
        return {
            'has_timezone': False,
            'timezone_name': None,
            'utc_offset': None,
            'is_dst': None
        }
    
    return {
        'has_timezone': True,
        'timezone_name': str(parsed_date.tzinfo),
        'utc_offset': parsed_date.utcoffset().total_seconds() if parsed_date.utcoffset() else None,
        'is_dst': parsed_date.dst() is not None and parsed_date.dst().total_seconds() > 0
    }


def parse_datetime(datetime_str: str) -> Dict[str, Any]:
    """
    Parse a datetime string and return detailed information.
    
    Args:
        datetime_str (str): Datetime string to parse
        
    Returns:
        dict: Detailed datetime information
    """
    parsed_date = parser.parse(datetime_str)
    
    return {
        'year': parsed_date.year,
        'month': parsed_date.month,
        'day': parsed_date.day,
        'hour': parsed_date.hour,
        'minute': parsed_date.minute,
        'second': parsed_date.second,
        'microsecond': parsed_date.microsecond,
        'weekday': parsed_date.weekday(),  # 0=Monday, 6=Sunday
        'weekday_name': parsed_date.strftime('%A'),
        'month_name': parsed_date.strftime('%B'),
        'iso_format': parsed_date.isoformat(),
        'unix_timestamp': int(parsed_date.timestamp()) if parsed_date.tzinfo else None
    }


def is_valid_datetime(datetime_str: str) -> bool:
    """
    Check if a string can be parsed as a datetime.
    
    Args:
        datetime_str (str): String to validate
        
    Returns:
        bool: True if valid datetime string
        
    Examples:
        >>> is_valid_datetime("2021-01-01")
        True
        >>> is_valid_datetime("invalid-date")
        False
    """
    try:
        parser.parse(datetime_str)
        return True
    except (ValueError, TypeError):
        return False


def get_current_unix() -> int:
    """
    Get current Unix timestamp.
    
    Returns:
        int: Current Unix timestamp
    """
    return int(time.time())


def get_current_datetime(format_str: str = "%Y-%m-%d %H:%M:%S",
                        timezone_str: Optional[str] = None) -> str:
    """
    Get current datetime as formatted string.
    
    Args:
        format_str (str): Output format
        timezone_str (str, optional): Timezone
        
    Returns:
        str: Current datetime string
    """
    now = datetime.now(timezone.utc)
    
    if timezone_str:
        import pytz
        tz = pytz.timezone(timezone_str)
        now = now.astimezone(tz)
    
    return now.strftime(format_str)


def convert_timezone(datetime_str: str, 
                    from_timezone: str,
                    to_timezone: str,
                    format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Convert datetime from one timezone to another.
    
    Args:
        datetime_str (str): Input datetime string
        from_timezone (str): Source timezone
        to_timezone (str): Target timezone
        format_str (str): Output format
        
    Returns:
        str: Converted datetime string
    """
    import pytz
    
    parsed_date = parser.parse(datetime_str)
    
    # Set source timezone
    from_tz = pytz.timezone(from_timezone)
    if parsed_date.tzinfo is None:
        parsed_date = from_tz.localize(parsed_date)
    
    # Convert to target timezone
    to_tz = pytz.timezone(to_timezone)
    converted_date = parsed_date.astimezone(to_tz)
    
    return converted_date.strftime(format_str)


def get_date_range(start_date: str, end_date: str, 
                  step_days: int = 1) -> List[str]:
    """
    Generate a list of dates between start and end dates.
    
    Args:
        start_date (str): Start date string
        end_date (str): End date string
        step_days (int): Step size in days
        
    Returns:
        list: List of date strings
    """
    start_dt = parser.parse(start_date).date()
    end_dt = parser.parse(end_date).date()
    
    dates = []
    current_date = start_dt
    
    while current_date <= end_dt:
        dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=step_days)
    
    return dates


def calculate_age(birth_date: str, reference_date: Optional[str] = None) -> Dict[str, int]:
    """
    Calculate age from birth date.
    
    Args:
        birth_date (str): Birth date string
        reference_date (str, optional): Reference date (default: today)
        
    Returns:
        dict: Age in years, months, and days
    """
    birth_dt = parser.parse(birth_date).date()
    
    if reference_date:
        ref_dt = parser.parse(reference_date).date()
    else:
        ref_dt = datetime.now().date()
    
    age = relativedelta(ref_dt, birth_dt)
    
    return {
        'years': age.years,
        'months': age.months,
        'days': age.days,
        'total_days': (ref_dt - birth_dt).days
    }


def get_weekday(datetime_str: str) -> Dict[str, Union[int, str]]:
    """
    Get weekday information from datetime string.
    
    Args:
        datetime_str (str): Datetime string
        
    Returns:
        dict: Weekday information
    """
    parsed_date = parser.parse(datetime_str)
    
    return {
        'weekday_number': parsed_date.weekday(),  # 0=Monday, 6=Sunday
        'weekday_name': parsed_date.strftime('%A'),
        'weekday_short': parsed_date.strftime('%a'),
        'is_weekend': parsed_date.weekday() >= 5
    }


def is_weekend(datetime_str: str) -> bool:
    """
    Check if the date falls on a weekend.
    
    Args:
        datetime_str (str): Datetime string
        
    Returns:
        bool: True if weekend (Saturday or Sunday)
    """
    parsed_date = parser.parse(datetime_str)
    return parsed_date.weekday() >= 5


def get_quarter(datetime_str: str) -> Dict[str, Union[int, str]]:
    """
    Get quarter information from datetime string.
    
    Args:
        datetime_str (str): Datetime string
        
    Returns:
        dict: Quarter information
    """
    parsed_date = parser.parse(datetime_str)
    quarter = (parsed_date.month - 1) // 3 + 1
    
    return {
        'quarter': quarter,
        'quarter_name': f'Q{quarter}',
        'year': parsed_date.year,
        'quarter_start_month': (quarter - 1) * 3 + 1,
        'quarter_end_month': quarter * 3
    }


def round_datetime(datetime_str: str, 
                  round_to: str = 'hour') -> str:
    """
    Round datetime to specified precision.
    
    Args:
        datetime_str (str): Input datetime string
        round_to (str): Round to 'year', 'month', 'day', 'hour', 'minute', or 'second'
        
    Returns:
        str: Rounded datetime string
    """
    parsed_date = parser.parse(datetime_str)
    
    if round_to == 'year':
        rounded = parsed_date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    elif round_to == 'month':
        rounded = parsed_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif round_to == 'day':
        rounded = parsed_date.replace(hour=0, minute=0, second=0, microsecond=0)
    elif round_to == 'hour':
        rounded = parsed_date.replace(minute=0, second=0, microsecond=0)
    elif round_to == 'minute':
        rounded = parsed_date.replace(second=0, microsecond=0)
    elif round_to == 'second':
        rounded = parsed_date.replace(microsecond=0)
    else:
        raise ValueError(f"Invalid round_to value: {round_to}")
    
    return rounded.strftime("%Y-%m-%d %H:%M:%S")
