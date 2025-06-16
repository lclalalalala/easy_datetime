#!/usr/bin/env python3
"""
Easy DateTime Examples - Comprehensive demonstration of all features.

This script demonstrates all the functionality provided by the easy_datetime package.
"""

import easy_datetime as edt


def main():
    print("🚀 Easy DateTime - Comprehensive Examples")
    print("=" * 50)
    
    # Basic conversion examples
    print("\n📅 Basic Conversions:")
    print(f"to_unix('2021-01-01'): {edt.to_unix('2021-01-01')}")
    print(f"from_unix(1609459200): {edt.from_unix(1609459200)}")
    print(f"format_datetime('2021-01-01', '%B %d, %Y'): {edt.format_datetime('2021-01-01', '%B %d, %Y')}")
    
    # Date arithmetic
    print("\n➕ Date Arithmetic:")
    print(f"add_time('2021-01-01', days=30): {edt.add_time('2021-01-01', days=30)}")
    print(f"subtract_time('2021-01-31', days=30): {edt.subtract_time('2021-01-31', days=30)}")
    print(f"add_time('2021-01-01', years=1, months=6): {edt.add_time('2021-01-01', years=1, months=6)}")
    
    # Date comparison
    print("\n📊 Date Comparison:")
    comparison = edt.compare_dates("2021-01-01", "2021-01-02")
    print(f"compare_dates('2021-01-01', '2021-01-02'):")
    print(f"  - Difference in days: {comparison['difference_days']}")
    print(f"  - Date1 before Date2: {comparison['date1_before_date2']}")
    print(f"  - Difference in hours: {comparison['difference_hours']}")
    
    # Timezone operations
    print("\n🌍 Timezone Operations:")
    try:
        tz_converted = edt.convert_timezone("2021-01-01 12:00:00", "UTC", "US/Eastern")
        print(f"convert_timezone('2021-01-01 12:00:00', 'UTC', 'US/Eastern'): {tz_converted}")
    except Exception as e:
        print(f"Timezone conversion example (requires pytz): {e}")
    
    # Parsing and validation
    print("\n🔍 Parsing and Validation:")
    parsed = edt.parse_datetime("2021-01-01 12:30:45")
    print(f"parse_datetime('2021-01-01 12:30:45'):")
    print(f"  - Year: {parsed['year']}, Month: {parsed['month']}, Day: {parsed['day']}")
    print(f"  - Weekday: {parsed['weekday_name']}")
    print(f"  - Month name: {parsed['month_name']}")
    
    print(f"is_valid_datetime('2021-01-01'): {edt.is_valid_datetime('2021-01-01')}")
    print(f"is_valid_datetime('invalid-date'): {edt.is_valid_datetime('invalid-date')}")
    
    # Current time functions
    print("\n⏰ Current Time:")
    print(f"get_current_unix(): {edt.get_current_unix()}")
    print(f"get_current_datetime(): {edt.get_current_datetime()}")
    print(f"get_current_datetime('%Y-%m-%d'): {edt.get_current_datetime('%Y-%m-%d')}")
    
    # Date ranges
    print("\n📈 Date Ranges:")
    date_range = edt.get_date_range("2021-01-01", "2021-01-05")
    print(f"get_date_range('2021-01-01', '2021-01-05'): {date_range}")
    
    date_range_step = edt.get_date_range("2021-01-01", "2021-01-10", step_days=3)
    print(f"get_date_range('2021-01-01', '2021-01-10', step_days=3): {date_range_step}")
    
    # Age calculation
    print("\n🎂 Age Calculation:")
    age = edt.calculate_age("1990-01-01", "2021-01-01")
    print(f"calculate_age('1990-01-01', '2021-01-01'):")
    print(f"  - Years: {age['years']}, Months: {age['months']}, Days: {age['days']}")
    print(f"  - Total days: {age['total_days']}")
    
    # Weekday functions
    print("\n📆 Weekday Functions:")
    weekday_info = edt.get_weekday("2021-01-01")
    print(f"get_weekday('2021-01-01'):")
    print(f"  - Weekday name: {weekday_info['weekday_name']}")
    print(f"  - Is weekend: {weekday_info['is_weekend']}")
    
    print(f"is_weekend('2021-01-02'): {edt.is_weekend('2021-01-02')} (Saturday)")
    print(f"is_weekend('2021-01-01'): {edt.is_weekend('2021-01-01')} (Friday)")
    
    # Quarter information
    print("\n📊 Quarter Information:")
    quarter_info = edt.get_quarter("2021-03-15")
    print(f"get_quarter('2021-03-15'):")
    print(f"  - Quarter: {quarter_info['quarter_name']}")
    print(f"  - Year: {quarter_info['year']}")
    
    # Datetime rounding
    print("\n🎯 Datetime Rounding:")
    print(f"round_datetime('2021-01-01 12:34:56', 'hour'): {edt.round_datetime('2021-01-01 12:34:56', 'hour')}")
    print(f"round_datetime('2021-01-15 12:34:56', 'month'): {edt.round_datetime('2021-01-15 12:34:56', 'month')}")
    print(f"round_datetime('2021-06-15 12:34:56', 'year'): {edt.round_datetime('2021-06-15 12:34:56', 'year')}")
    
    # Timezone info
    print("\n🌐 Timezone Information:")
    tz_info_none = edt.get_timezone_info("2021-01-01")
    print(f"get_timezone_info('2021-01-01'): {tz_info_none}")
    
    tz_info_with = edt.get_timezone_info("2021-01-01T12:00:00+05:00")
    print(f"get_timezone_info('2021-01-01T12:00:00+05:00'): {tz_info_with}")
    
    # Edge cases and format examples
    print("\n🔧 Format Examples:")
    formats = [
        "2021-01-01",
        "2021/01/01", 
        "01-01-2021",
        "January 1, 2021",
        "2021-01-01 12:30:45",
        "2021-01-01T12:30:45Z"
    ]
    
    for fmt in formats:
        try:
            unix_time = edt.to_unix(fmt)
            print(f"'{fmt}' -> {unix_time}")
        except Exception as e:
            print(f"'{fmt}' -> Error: {e}")
    
    print("\n✅ All examples completed successfully!")
    print("\n📚 For more information, see the README.md file or visit:")
    print("   https://github.com/lclalalalala/easy_datetime")


if __name__ == "__main__":
    main()