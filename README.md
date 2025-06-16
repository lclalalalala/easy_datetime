# Easy DateTime

A comprehensive Python package for datetime manipulation, conversion, and formatting. 
处理日期字符串真的是蛋疼。让我们一劳永逸地解决这个问题。

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI Version](https://img.shields.io/badge/pypi-v1.0.0-orange.svg)](https://pypi.org)

## 🚀 Features

- **🔄 Automatic datetime string format detection** - Parse any common datetime format
- **⏰ Unix timestamp conversion** - Convert to/from Unix timestamps effortlessly  
- **🌍 Timezone support** - Handle timezones with ease
- **📅 Date arithmetic** - Add/subtract time periods
- **📊 Date comparison** - Compare dates and get detailed differences
- **🎯 Format conversion** - Convert between any datetime formats
- **📈 Date ranges** - Generate date sequences
- **🔍 Validation** - Check if strings are valid datetime formats
- **📆 Calendar utilities** - Weekdays, quarters, age calculation
- **⚡ High performance** - Optimized for speed and memory efficiency

## 📦 Installation

```bash
# Install from PyPI
pip install easy-datetime

# Install with development dependencies
pip install easy-datetime[dev]

# Install from source
git clone https://github.com/lclalalalala/easy_datetime.git
cd easy_datetime
pip install -e .
```

## 🎯 Quick Start

```python
import easy_datetime as edt

# Convert datetime strings to Unix timestamps
timestamp = edt.to_unix("2021-01-01")                    # 1609459200
timestamp = edt.to_unix("2021/01/01 12:00:00")          # 1609502400
timestamp = edt.to_unix("01-01-2021", "US/Eastern")     # With timezone

# Convert Unix timestamps back to datetime strings
date_str = edt.from_unix(1609459200)                    # "2021-01-01 00:00:00"
date_str = edt.from_unix(1609459200, "%Y/%m/%d")        # "2021/01/01"

# Format datetime strings
formatted = edt.format_datetime("2021-01-01", "%B %d, %Y")  # "January 01, 2021"

# Add/subtract time
future = edt.add_time("2021-01-01", days=30, hours=12)      # "2021-01-31 12:00:00"
past = edt.subtract_time("2021-01-31", days=30)             # "2021-01-01 00:00:00"

# Compare dates
diff = edt.compare_dates("2021-01-01", "2021-01-02")
print(diff['difference_days'])  # 1
print(diff['date1_before_date2'])  # True

# Validate datetime strings
is_valid = edt.is_valid_datetime("2021-01-01")              # True
is_valid = edt.is_valid_datetime("invalid-date")            # False
```

## 📚 Comprehensive API

### Core Conversion Functions

```python
# Unix timestamp conversion
edt.to_unix(datetime_str, timezone_str=None)
edt.from_unix(timestamp, format_str="%Y-%m-%d %H:%M:%S", timezone_str=None)

# Format conversion
edt.format_datetime(datetime_str, output_format="%Y-%m-%d %H:%M:%S", 
                   input_timezone=None, output_timezone=None)
```

### Date Arithmetic

```python
# Add time periods
edt.add_time(datetime_str, years=0, months=0, days=0, hours=0, minutes=0, seconds=0)

# Subtract time periods  
edt.subtract_time(datetime_str, years=0, months=0, days=0, hours=0, minutes=0, seconds=0)

# Examples
future_date = edt.add_time("2021-01-01", years=1, months=6, days=15)
past_date = edt.subtract_time("2021-12-31", months=11, days=30)
```

### Date Comparison & Analysis

```python
# Compare two dates
comparison = edt.compare_dates("2021-01-01", "2021-01-02")
# Returns: {
#     'difference_days': 1,
#     'difference_seconds': 86400,
#     'difference_hours': 24.0,
#     'date1_before_date2': True,
#     'dates_equal': False,
#     ...
# }

# Parse datetime details
details = edt.parse_datetime("2021-01-01 12:30:45")
# Returns: {
#     'year': 2021, 'month': 1, 'day': 1,
#     'hour': 12, 'minute': 30, 'second': 45,
#     'weekday_name': 'Friday', 'month_name': 'January',
#     ...
# }
```

### Timezone Operations

```python
# Get timezone information
tz_info = edt.get_timezone_info("2021-01-01T12:00:00+05:00")

# Convert between timezones
converted = edt.convert_timezone("2021-01-01 12:00:00", "UTC", "US/Eastern")

# Current time in different timezones
current_utc = edt.get_current_datetime()
current_est = edt.get_current_datetime(timezone_str="US/Eastern")
```

### Utility Functions

```python
# Generate date ranges
dates = edt.get_date_range("2021-01-01", "2021-01-05")
# Returns: ['2021-01-01', '2021-01-02', '2021-01-03', '2021-01-04', '2021-01-05']

# Calculate age
age = edt.calculate_age("1990-01-01", "2021-01-01")
# Returns: {'years': 31, 'months': 0, 'days': 0, 'total_days': 11323}

# Weekday information
weekday = edt.get_weekday("2021-01-01")
# Returns: {'weekday_number': 4, 'weekday_name': 'Friday', 'is_weekend': False}

# Check if weekend
is_weekend = edt.is_weekend("2021-01-02")  # True (Saturday)

# Quarter information
quarter = edt.get_quarter("2021-03-15")
# Returns: {'quarter': 1, 'quarter_name': 'Q1', 'year': 2021}

# Round datetime
rounded = edt.round_datetime("2021-01-01 12:34:56", "hour")  # "2021-01-01 12:00:00"
```

### Validation & Current Time

```python
# Validate datetime strings
edt.is_valid_datetime("2021-01-01")      # True
edt.is_valid_datetime("invalid-date")    # False

# Get current time
current_unix = edt.get_current_unix()    # Current Unix timestamp
current_time = edt.get_current_datetime()  # Current datetime string
```

## 🌍 Timezone Support

Easy DateTime supports comprehensive timezone handling:

```python
# Parse with timezone
timestamp = edt.to_unix("2021-01-01 12:00:00", "US/Eastern")

# Convert between timezones
tokyo_time = edt.convert_timezone(
    "2021-01-01 12:00:00", 
    from_timezone="UTC", 
    to_timezone="Asia/Tokyo"
)

# Format with timezone conversion
formatted = edt.format_datetime(
    "2021-01-01 12:00:00",
    output_format="%Y-%m-%d %H:%M:%S %Z",
    input_timezone="UTC",
    output_timezone="Europe/London"
)
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Install test dependencies
pip install easy-datetime[test]

# Run all tests
pytest

# Run with coverage
pytest --cov=easy_datetime

# Run performance tests
pytest tests/test_performance.py -v
```

## 🛠️ Development

Set up development environment:

```bash
# Clone the repository
git clone https://github.com/lclalalalala/easy_datetime.git
cd easy_datetime

# Install in development mode with all dependencies
pip install -e .[dev]

# Run code formatting
black easy_datetime tests
isort easy_datetime tests

# Run type checking
mypy easy_datetime

# Run linting
flake8 easy_datetime tests
```

## 📋 Supported Formats

Easy DateTime automatically detects and parses many datetime formats:

- **ISO formats**: `2021-01-01`, `2021-01-01T12:00:00`, `2021-01-01T12:00:00Z`
- **US formats**: `01/01/2021`, `01-01-2021`, `January 1, 2021`
- **European formats**: `01.01.2021`, `1/1/2021`
- **Relative formats**: `today`, `yesterday`, `tomorrow`
- **With timezones**: `2021-01-01 12:00:00+05:00`, `2021-01-01 12:00:00 EST`

## ⚡ Performance

Easy DateTime is optimized for performance:

- **Fast parsing**: Handles 1000+ datetime conversions per second
- **Memory efficient**: Minimal memory footprint
- **Timezone caching**: Efficient timezone operations
- **Lazy imports**: Only loads what you need

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on top of the excellent [python-dateutil](https://github.com/dateutil/dateutil) library
- Timezone support powered by [pytz](https://pythonhosted.org/pytz/)
- Inspired by the need for a simple, comprehensive datetime utility

## 📞 Support

- 📧 Email: lucy@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/lclalalalala/easy_datetime/issues)
- 📖 Documentation: [GitHub README](https://github.com/lclalalalala/easy_datetime#readme)