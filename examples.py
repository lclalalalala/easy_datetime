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
    
    # Chinese date support examples
    print("\n🇨🇳 Chinese Date Support:")
    
    # Parse Chinese dates
    chinese_dates = [
        "二〇二一年一月一日",
        "民国一一〇年三月十五日", 
        "2021年12月31日",
        "正月初一"
    ]
    
    for chinese_date in chinese_dates:
        try:
            parsed = edt.parse_chinese_date(chinese_date)
            print(f"parse_chinese_date('{chinese_date}'):")
            print(f"  - Year: {parsed['year']}, Month: {parsed['month']}, Day: {parsed['day']}")
            print(f"  - Weekday: {parsed['weekday_chinese']}")
            if parsed['era']:
                print(f"  - Era: {parsed['era']}")
        except Exception as e:
            print(f"'{chinese_date}' -> Error: {e}")
    
    # Format Chinese dates
    print(f"\nformat_chinese_date('2021-01-01', 'full'): {edt.format_chinese_date('2021-01-01', 'full')}")
    print(f"format_chinese_date('2021-01-01', 'short'): {edt.format_chinese_date('2021-01-01', 'short')}")
    print(f"format_chinese_date('2021-01-01', use_era='民国'): {edt.format_chinese_date('2021-01-01', use_era='民国')}")
    
    # Chinese Unix conversion
    print(f"\nto_unix_chinese('二〇二一年一月一日'): {edt.to_unix_chinese('二〇二一年一月一日')}")
    print(f"from_unix_chinese(1609459200): {edt.from_unix_chinese(1609459200)}")
    
    # Chinese utilities
    print(f"\nget_chinese_weekday('2021-01-01'): {edt.get_chinese_weekday('2021-01-01')}")
    print(f"get_chinese_weekday('2021-01-01', short=True): {edt.get_chinese_weekday('2021-01-01', short=True)}")
    print(f"get_chinese_month(1): {edt.get_chinese_month(1)}")
    print(f"get_chinese_month(12): {edt.get_chinese_month(12)}")
    
    # Era conversion
    print(f"\nconvert_chinese_era(110, '民国', '公元'): {edt.convert_chinese_era(110, '民国', '公元')}")
    print(f"convert_chinese_era(2021, '公元', '民国'): {edt.convert_chinese_era(2021, '公元', '民国')}")
    
    # Validation
    print(f"\nis_valid_chinese_date('二〇二一年一月一日'): {edt.is_valid_chinese_date('二〇二一年一月一日')}")
    print(f"is_valid_chinese_date('无效日期'): {edt.is_valid_chinese_date('无效日期')}")

    print("\n✅ All examples completed successfully!")
    print("\n📚 For more information, see the README.md file or visit:")
    print("   https://github.com/lclalalalala/easy_datetime")


if __name__ == "__main__":
    main()