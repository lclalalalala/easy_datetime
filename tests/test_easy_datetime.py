"""
Comprehensive test suite for easy_datetime package.
"""

import pytest
from datetime import datetime, timezone
import easy_datetime as edt


class TestToUnix:
    """Test the to_unix function."""
    
    def test_standard_format(self):
        assert edt.to_unix("2021-01-01") == 1609459200
        
    def test_slash_format(self):
        assert edt.to_unix("2021/01/01") == 1609459200
        
    def test_american_format(self):
        assert edt.to_unix("01-01-2021") == 1609459200
        
    def test_short_format(self):
        assert edt.to_unix("1-01-2021") == 1609459200
        
    def test_with_time(self):
        assert edt.to_unix("2021-01-01 12:00:00") == 1609502400
        
    def test_with_timezone(self):
        # Test with timezone string
        result = edt.to_unix("2021-01-01 00:00:00", "US/Eastern")
        assert isinstance(result, int)
        
    def test_invalid_format(self):
        with pytest.raises(ValueError, match="Could not parse datetime string"):
            edt.to_unix("invalid-date")
            
    def test_empty_string(self):
        with pytest.raises(ValueError):
            edt.to_unix("")
            
    def test_none_input(self):
        with pytest.raises(ValueError):
            edt.to_unix(None)


class TestFromUnix:
    """Test the from_unix function."""
    
    def test_basic_conversion(self):
        result = edt.from_unix(1609459200)
        assert result == "2021-01-01 00:00:00"
        
    def test_custom_format(self):
        result = edt.from_unix(1609459200, "%Y/%m/%d")
        assert result == "2021/01/01"
        
    def test_with_timezone(self):
        result = edt.from_unix(1609459200, timezone_str="US/Eastern")
        assert "2020-12-31" in result  # Should be previous day in Eastern time
        
    def test_float_timestamp(self):
        result = edt.from_unix(1609459200.5)
        assert "2021-01-01" in result
        
    def test_invalid_timestamp(self):
        with pytest.raises(ValueError):
            edt.from_unix("invalid")


class TestFormatDatetime:
    """Test the format_datetime function."""
    
    def test_basic_formatting(self):
        result = edt.format_datetime("2021-01-01", "%B %d, %Y")
        assert result == "January 01, 2021"
        
    def test_timezone_conversion(self):
        result = edt.format_datetime(
            "2021-01-01 12:00:00",
            input_timezone="UTC",
            output_timezone="US/Eastern"
        )
        assert "07:00:00" in result  # 12:00 UTC = 07:00 EST
        
    def test_default_format(self):
        result = edt.format_datetime("2021-01-01")
        assert result == "2021-01-01 00:00:00"


class TestAddTime:
    """Test the add_time function."""
    
    def test_add_days(self):
        result = edt.add_time("2021-01-01", days=30)
        assert result == "2021-01-31 00:00:00"
        
    def test_add_hours(self):
        result = edt.add_time("2021-01-01", hours=12)
        assert result == "2021-01-01 12:00:00"
        
    def test_add_months(self):
        result = edt.add_time("2021-01-01", months=1)
        assert result == "2021-02-01 00:00:00"
        
    def test_add_years(self):
        result = edt.add_time("2021-01-01", years=1)
        assert result == "2022-01-01 00:00:00"
        
    def test_add_multiple_units(self):
        result = edt.add_time("2021-01-01", years=1, months=1, days=1, hours=1)
        assert result == "2022-02-02 01:00:00"


class TestSubtractTime:
    """Test the subtract_time function."""
    
    def test_subtract_days(self):
        result = edt.subtract_time("2021-01-31", days=30)
        assert result == "2021-01-01 00:00:00"
        
    def test_subtract_months(self):
        result = edt.subtract_time("2021-02-01", months=1)
        assert result == "2021-01-01 00:00:00"


class TestCompareDates:
    """Test the compare_dates function."""
    
    def test_date_comparison(self):
        result = edt.compare_dates("2021-01-01", "2021-01-02")
        assert result['difference_days'] == 1
        assert result['difference_seconds'] == 86400
        assert result['date1_before_date2'] is True
        assert result['date1_after_date2'] is False
        assert result['dates_equal'] is False
        
    def test_equal_dates(self):
        result = edt.compare_dates("2021-01-01", "2021-01-01")
        assert result['dates_equal'] is True
        assert result['difference_days'] == 0
        
    def test_reverse_comparison(self):
        result = edt.compare_dates("2021-01-02", "2021-01-01")
        assert result['date1_after_date2'] is True
        assert result['difference_days'] == -1


class TestTimezoneInfo:
    """Test the get_timezone_info function."""
    
    def test_no_timezone(self):
        result = edt.get_timezone_info("2021-01-01")
        assert result['has_timezone'] is False
        assert result['timezone_name'] is None
        
    def test_with_timezone(self):
        result = edt.get_timezone_info("2021-01-01T00:00:00+00:00")
        assert result['has_timezone'] is True


class TestParseDatetime:
    """Test the parse_datetime function."""
    
    def test_basic_parsing(self):
        result = edt.parse_datetime("2021-01-01 12:30:45")
        assert result['year'] == 2021
        assert result['month'] == 1
        assert result['day'] == 1
        assert result['hour'] == 12
        assert result['minute'] == 30
        assert result['second'] == 45
        assert result['weekday_name'] == 'Friday'
        assert result['month_name'] == 'January'


class TestValidation:
    """Test validation functions."""
    
    def test_is_valid_datetime_true(self):
        assert edt.is_valid_datetime("2021-01-01") is True
        assert edt.is_valid_datetime("2021/01/01") is True
        assert edt.is_valid_datetime("01-01-2021") is True
        
    def test_is_valid_datetime_false(self):
        assert edt.is_valid_datetime("invalid-date") is False
        assert edt.is_valid_datetime("2021-13-01") is False
        assert edt.is_valid_datetime("") is False


class TestCurrentTime:
    """Test current time functions."""
    
    def test_get_current_unix(self):
        result = edt.get_current_unix()
        assert isinstance(result, int)
        assert result > 0
        
    def test_get_current_datetime(self):
        result = edt.get_current_datetime()
        assert isinstance(result, str)
        assert len(result) == 19  # YYYY-MM-DD HH:MM:SS format
        
    def test_get_current_datetime_custom_format(self):
        result = edt.get_current_datetime("%Y-%m-%d")
        assert len(result) == 10  # YYYY-MM-DD format


class TestTimezoneConversion:
    """Test timezone conversion functions."""
    
    def test_convert_timezone(self):
        result = edt.convert_timezone(
            "2021-01-01 12:00:00",
            "UTC",
            "US/Eastern"
        )
        assert "07:00:00" in result  # UTC-5 for EST


class TestDateRange:
    """Test date range generation."""
    
    def test_basic_date_range(self):
        result = edt.get_date_range("2021-01-01", "2021-01-03")
        expected = ["2021-01-01", "2021-01-02", "2021-01-03"]
        assert result == expected
        
    def test_date_range_with_step(self):
        result = edt.get_date_range("2021-01-01", "2021-01-05", step_days=2)
        expected = ["2021-01-01", "2021-01-03", "2021-01-05"]
        assert result == expected


class TestAgeCalculation:
    """Test age calculation."""
    
    def test_calculate_age(self):
        result = edt.calculate_age("1990-01-01", "2021-01-01")
        assert result['years'] == 31
        assert result['months'] == 0
        assert result['days'] == 0
        
    def test_calculate_age_with_months(self):
        result = edt.calculate_age("1990-01-01", "2021-06-15")
        assert result['years'] == 31
        assert result['months'] == 5


class TestWeekdayFunctions:
    """Test weekday-related functions."""
    
    def test_get_weekday(self):
        result = edt.get_weekday("2021-01-01")  # Friday
        assert result['weekday_number'] == 4  # 0=Monday, 4=Friday
        assert result['weekday_name'] == 'Friday'
        assert result['weekday_short'] == 'Fri'
        assert result['is_weekend'] is False
        
    def test_is_weekend_false(self):
        assert edt.is_weekend("2021-01-01") is False  # Friday
        
    def test_is_weekend_true(self):
        assert edt.is_weekend("2021-01-02") is True  # Saturday
        assert edt.is_weekend("2021-01-03") is True  # Sunday


class TestQuarter:
    """Test quarter functions."""
    
    def test_get_quarter_q1(self):
        result = edt.get_quarter("2021-01-15")
        assert result['quarter'] == 1
        assert result['quarter_name'] == 'Q1'
        assert result['year'] == 2021
        
    def test_get_quarter_q4(self):
        result = edt.get_quarter("2021-12-15")
        assert result['quarter'] == 4
        assert result['quarter_name'] == 'Q4'


class TestRoundDatetime:
    """Test datetime rounding."""
    
    def test_round_to_hour(self):
        result = edt.round_datetime("2021-01-01 12:34:56", "hour")
        assert result == "2021-01-01 12:00:00"
        
    def test_round_to_day(self):
        result = edt.round_datetime("2021-01-01 12:34:56", "day")
        assert result == "2021-01-01 00:00:00"
        
    def test_round_to_month(self):
        result = edt.round_datetime("2021-01-15 12:34:56", "month")
        assert result == "2021-01-01 00:00:00"
        
    def test_round_to_year(self):
        result = edt.round_datetime("2021-06-15 12:34:56", "year")
        assert result == "2021-01-01 00:00:00"
        
    def test_invalid_round_to(self):
        with pytest.raises(ValueError, match="Invalid round_to value"):
            edt.round_datetime("2021-01-01", "invalid")


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_leap_year_handling(self):
        # Test leap year date
        result = edt.to_unix("2020-02-29")
        assert isinstance(result, int)
        
    def test_end_of_year(self):
        result = edt.add_time("2020-12-31", days=1)
        assert result == "2021-01-01 00:00:00"
        
    def test_february_edge_case(self):
        # Adding a month to January 31st
        result = edt.add_time("2021-01-31", months=1)
        assert "2021-02" in result  # Should handle February correctly
        
    def test_large_timestamp(self):
        # Test with a large timestamp
        large_timestamp = 2147483647  # Max 32-bit signed integer
        result = edt.from_unix(large_timestamp)
        assert isinstance(result, str)


if __name__ == '__main__':
    pytest.main([__file__])
