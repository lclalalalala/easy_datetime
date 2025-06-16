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
import locale

__version__ = "1.1.0"
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
    "round_datetime",
    # Chinese date support
    "parse_chinese_date",
    "format_chinese_date",
    "to_unix_chinese",
    "from_unix_chinese",
    "get_chinese_weekday",
    "get_chinese_month",
    "convert_chinese_era",
    "is_valid_chinese_date"
]

# Chinese date mappings
CHINESE_NUMBERS = {
    '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
    '十': 10, '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15, '十六': 16, '十七': 17, 
    '十八': 18, '十九': 19, '二十': 20, '二十一': 21, '二十二': 22, '二十三': 23, '二十四': 24,
    '二十五': 25, '二十六': 26, '二十七': 27, '二十八': 28, '二十九': 29, '三十': 30, '三十一': 31
}

CHINESE_MONTHS = {
    '一月': 1, '二月': 2, '三月': 3, '四月': 4, '五月': 5, '六月': 6,
    '七月': 7, '八月': 8, '九月': 9, '十月': 10, '十一月': 11, '十二月': 12,
    '正月': 1, '腊月': 12
}

CHINESE_WEEKDAYS = {
    0: '星期一', 1: '星期二', 2: '星期三', 3: '星期四', 4: '星期五', 5: '星期六', 6: '星期日'
}

CHINESE_WEEKDAYS_SHORT = {
    0: '周一', 1: '周二', 2: '周三', 3: '周四', 4: '周五', 5: '周六', 6: '周日'
}

MONTH_NAMES_CHINESE = {
    1: '一月', 2: '二月', 3: '三月', 4: '四月', 5: '五月', 6: '六月',
    7: '七月', 8: '八月', 9: '九月', 10: '十月', 11: '十一月', 12: '十二月'
}

# Chinese era mappings (simplified)
CHINESE_ERAS = {
    '民国': 1911,  # Republic of China era
    '公元': 0,     # Common Era
    '西元': 0      # Western Era
}


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


# Chinese date support functions

def _chinese_number_to_int(chinese_num: str) -> int:
    """Convert Chinese number to integer."""
    if chinese_num in CHINESE_NUMBERS:
        return CHINESE_NUMBERS[chinese_num]
    
    # Handle year format like 二〇二一 (each character is a digit)
    if len(chinese_num) >= 3 and all(c in ['零', '〇', '一', '二', '三', '四', '五', '六', '七', '八', '九'] for c in chinese_num):
        result = 0
        for char in chinese_num:
            digit_map = {'零': 0, '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
            if char in digit_map:
                result = result * 10 + digit_map[char]
        return result
    
    # Handle traditional Chinese numbers with 十
    if '十' in chinese_num:
        if chinese_num == '十':
            return 10
        elif chinese_num.startswith('十'):
            # 十一, 十二, etc.
            remainder = chinese_num[1:]
            if remainder in CHINESE_NUMBERS:
                return 10 + CHINESE_NUMBERS[remainder]
        elif chinese_num.endswith('十'):
            # 二十, 三十, etc.
            prefix = chinese_num[:-1]
            if prefix in CHINESE_NUMBERS:
                return CHINESE_NUMBERS[prefix] * 10
        else:
            # 二十一, 三十五, etc.
            parts = chinese_num.split('十')
            if len(parts) == 2 and parts[0] in CHINESE_NUMBERS and parts[1] in CHINESE_NUMBERS:
                return CHINESE_NUMBERS[parts[0]] * 10 + CHINESE_NUMBERS[parts[1]]
    
    # Try to parse as regular number
    try:
        return int(chinese_num)
    except ValueError:
        raise ValueError(f"Cannot convert Chinese number: {chinese_num}")


def _int_to_chinese_number(num: int) -> str:
    """Convert integer to Chinese number."""
    if num == 0:
        return '零'
    
    chinese_digits = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
    
    if num < 10:
        return chinese_digits[num]
    elif num < 20:
        if num == 10:
            return '十'
        else:
            return '十' + chinese_digits[num - 10]
    elif num < 100:
        tens = num // 10
        ones = num % 10
        if ones == 0:
            return chinese_digits[tens] + '十'
        else:
            return chinese_digits[tens] + '十' + chinese_digits[ones]
    else:
        # For larger numbers, use a more complex conversion
        return str(num)  # Fallback to Arabic numerals


def parse_chinese_date(chinese_date_str: str) -> Dict[str, Any]:
    """
    Parse Chinese date string and return detailed information.
    
    Args:
        chinese_date_str (str): Chinese date string (e.g., "二〇二一年一月一日")
        
    Returns:
        dict: Parsed date information
        
    Examples:
        >>> parse_chinese_date("二〇二一年一月一日")
        {'year': 2021, 'month': 1, 'day': 1, 'datetime': datetime(...)}
        >>> parse_chinese_date("民国一一〇年三月十五日")
        {'year': 2021, 'month': 3, 'day': 15, 'era': '民国', 'datetime': datetime(...)}
    """
    # Remove common punctuation and spaces
    cleaned = chinese_date_str.strip().replace('，', '').replace('。', '').replace(' ', '')
    
    # Pattern for Chinese date formats
    patterns = [
        # 民国一一〇年三月十五日 (era patterns first)
        r'(民国|公元|西元)([一二三四五六七八九十零〇]{1,4})年(正月|腊月|[一二三四五六七八九十]{1,2}月)([一二三四五六七八九十初]{1,3})日?',
        # 二〇二一年正月初一 or 二〇二一年一月一日
        r'([一二三四五六七八九零〇]{2,4})年(正月|腊月|[一二三四五六七八九十]{1,2}月)([一二三四五六七八九十初]{1,3})日?',
        # 2021年1月1日 or 2021年一月一日
        r'(\d{4})年(正月|腊月|[一二三四五六七八九十\d]{1,3}月)([一二三四五六七八九十初\d]{1,3})日?',
        # 正月初一 (current year assumed)
        r'(正月|腊月|[一二三四五六七八九十]{1,2}月)([一二三四五六七八九十初]{1,3})日?'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, cleaned)
        if match:
            groups = match.groups()
            
            if len(groups) == 3:  # Year, month, day
                year_str, month_str, day_str = groups
                era = None
            elif len(groups) == 4:  # Era, year, month, day or just month, day
                if groups[0] in CHINESE_ERAS:  # Era format
                    era, year_str, month_str, day_str = groups
                else:  # Year, month, day, extra
                    year_str, month_str, day_str = groups[:3]
                    era = None
            elif len(groups) == 2:  # Month, day only
                month_str, day_str = groups
                year_str = str(datetime.now().year)
                era = None
            else:
                continue
            
            try:
                # Parse year
                if era in CHINESE_ERAS:
                    if era == '民国':
                        roc_year = _chinese_number_to_int(year_str)
                        year = 1911 + roc_year  # Convert ROC year to CE year
                    else:
                        year = _chinese_number_to_int(year_str)
                else:
                    year = _chinese_number_to_int(year_str)
                
                # Parse month
                if month_str in CHINESE_MONTHS:
                    month = CHINESE_MONTHS[month_str]
                elif month_str.endswith('月'):
                    month_part = month_str[:-1]
                    if month_part in CHINESE_MONTHS:
                        month = CHINESE_MONTHS[month_part]
                    else:
                        month = _chinese_number_to_int(month_part)
                else:
                    month = _chinese_number_to_int(month_str)
                
                # Parse day
                if day_str.startswith('初'):
                    # Handle 初一, 初二, etc.
                    day_part = day_str[1:]
                    if day_part == '':
                        day = 1  # 初 alone means 1st
                    else:
                        day = _chinese_number_to_int(day_part)
                else:
                    day = _chinese_number_to_int(day_str)
                
                # Create datetime object
                dt = datetime(year, month, day)
                
                return {
                    'year': year,
                    'month': month,
                    'day': day,
                    'era': era,
                    'datetime': dt,
                    'weekday': dt.weekday(),
                    'weekday_chinese': CHINESE_WEEKDAYS[dt.weekday()],
                    'month_chinese': MONTH_NAMES_CHINESE[month],
                    'iso_format': dt.isoformat()
                }
                
            except (ValueError, KeyError) as e:
                continue
    
    raise ValueError(f"Cannot parse Chinese date: {chinese_date_str}")


def format_chinese_date(datetime_obj: Union[datetime, str], 
                       format_type: str = 'full',
                       use_era: Optional[str] = None) -> str:
    """
    Format datetime as Chinese date string.
    
    Args:
        datetime_obj (datetime|str): Datetime object or string
        format_type (str): Format type ('full', 'short', 'traditional')
        use_era (str, optional): Era to use ('民国', '公元', '西元')
        
    Returns:
        str: Chinese formatted date string
        
    Examples:
        >>> format_chinese_date(datetime(2021, 1, 1))
        '二〇二一年一月一日'
        >>> format_chinese_date("2021-01-01", "short")
        '2021年1月1日'
        >>> format_chinese_date("2021-01-01", use_era="民国")
        '民国一一〇年一月一日'
    """
    if isinstance(datetime_obj, str):
        dt = parser.parse(datetime_obj)
    else:
        dt = datetime_obj
    
    year = dt.year
    month = dt.month
    day = dt.day
    
    if use_era == '民国':
        era_year = year - 1911
        if format_type == 'full':
            # Convert era year to Chinese format like 一一〇
            era_chinese = ''
            for digit in str(era_year):
                era_chinese += ['〇', '一', '二', '三', '四', '五', '六', '七', '八', '九'][int(digit)]
            year_str = '民国' + era_chinese + '年'
        else:
            year_str = f'民国{era_year}年'
    elif use_era in ['公元', '西元']:
        if format_type == 'full':
            year_str = use_era + _int_to_chinese_number(year) + '年'
        else:
            year_str = f'{use_era}{year}年'
    else:
        if format_type == 'full':
            # Convert year to Chinese characters
            year_chinese = ''
            for digit in str(year):
                if digit == '0':
                    year_chinese += '〇'
                else:
                    year_chinese += ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九'][int(digit)]
            year_str = year_chinese + '年'
        elif format_type == 'short':
            year_str = f'{year}年'
        else:  # traditional
            year_str = _int_to_chinese_number(year) + '年'
    
    if format_type == 'full':
        month_str = MONTH_NAMES_CHINESE[month]
        day_str = _int_to_chinese_number(day) + '日'
    elif format_type == 'short':
        month_str = f'{month}月'
        day_str = f'{day}日'
    else:  # traditional
        month_str = MONTH_NAMES_CHINESE[month]
        day_str = _int_to_chinese_number(day) + '日'
    
    return year_str + month_str + day_str


def to_unix_chinese(chinese_date_str: str, timezone_str: Optional[str] = None) -> int:
    """
    Convert Chinese date string to Unix timestamp.
    
    Args:
        chinese_date_str (str): Chinese date string
        timezone_str (str, optional): Timezone string
        
    Returns:
        int: Unix timestamp
        
    Examples:
        >>> to_unix_chinese("二〇二一年一月一日")
        1609459200
        >>> to_unix_chinese("民国一一〇年一月一日")
        1609459200
    """
    parsed = parse_chinese_date(chinese_date_str)
    dt = parsed['datetime']
    
    if timezone_str:
        import pytz
        tz = pytz.timezone(timezone_str)
        dt = tz.localize(dt)
    else:
        dt = dt.replace(tzinfo=timezone.utc)
    
    return int(dt.timestamp())


def from_unix_chinese(timestamp: Union[int, float], 
                     format_type: str = 'full',
                     use_era: Optional[str] = None,
                     timezone_str: Optional[str] = None) -> str:
    """
    Convert Unix timestamp to Chinese date string.
    
    Args:
        timestamp (int|float): Unix timestamp
        format_type (str): Format type ('full', 'short', 'traditional')
        use_era (str, optional): Era to use
        timezone_str (str, optional): Timezone string
        
    Returns:
        str: Chinese formatted date string
        
    Examples:
        >>> from_unix_chinese(1609459200)
        '二〇二一年一月一日'
    """
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    
    if timezone_str:
        import pytz
        tz = pytz.timezone(timezone_str)
        dt = dt.astimezone(tz)
    
    return format_chinese_date(dt, format_type, use_era)


def get_chinese_weekday(datetime_str: str, short: bool = False) -> str:
    """
    Get Chinese weekday name from datetime string.
    
    Args:
        datetime_str (str): Datetime string
        short (bool): Use short format (周一 vs 星期一)
        
    Returns:
        str: Chinese weekday name
        
    Examples:
        >>> get_chinese_weekday("2021-01-01")
        '星期五'
        >>> get_chinese_weekday("2021-01-01", short=True)
        '周五'
    """
    dt = parser.parse(datetime_str)
    weekday_num = dt.weekday()
    
    if short:
        return CHINESE_WEEKDAYS_SHORT[weekday_num]
    else:
        return CHINESE_WEEKDAYS[weekday_num]


def get_chinese_month(month_num: int) -> str:
    """
    Get Chinese month name from month number.
    
    Args:
        month_num (int): Month number (1-12)
        
    Returns:
        str: Chinese month name
        
    Examples:
        >>> get_chinese_month(1)
        '一月'
        >>> get_chinese_month(12)
        '十二月'
    """
    if month_num not in MONTH_NAMES_CHINESE:
        raise ValueError(f"Invalid month number: {month_num}")
    
    return MONTH_NAMES_CHINESE[month_num]


def convert_chinese_era(year: int, from_era: str, to_era: str) -> int:
    """
    Convert year between different Chinese eras.
    
    Args:
        year (int): Year in source era
        from_era (str): Source era ('民国', '公元', '西元')
        to_era (str): Target era ('民国', '公元', '西元')
        
    Returns:
        int: Year in target era
        
    Examples:
        >>> convert_chinese_era(110, '民国', '公元')
        2021
        >>> convert_chinese_era(2021, '公元', '民国')
        110
    """
    if from_era not in CHINESE_ERAS or to_era not in CHINESE_ERAS:
        raise ValueError("Invalid era specified")
    
    # Convert to Common Era first
    if from_era == '民国':
        ce_year = year + 1911
    else:  # 公元 or 西元
        ce_year = year
    
    # Convert from Common Era to target
    if to_era == '民国':
        return ce_year - 1911
    else:  # 公元 or 西元
        return ce_year


def is_valid_chinese_date(chinese_date_str: str) -> bool:
    """
    Check if a Chinese date string is valid.
    
    Args:
        chinese_date_str (str): Chinese date string to validate
        
    Returns:
        bool: True if valid Chinese date string
        
    Examples:
        >>> is_valid_chinese_date("二〇二一年一月一日")
        True
        >>> is_valid_chinese_date("无效日期")
        False
    """
    try:
        parse_chinese_date(chinese_date_str)
        return True
    except (ValueError, TypeError):
        return False
