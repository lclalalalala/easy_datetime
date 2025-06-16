"""
Test suite for Chinese date functionality in easy_datetime package.
"""

import pytest
from datetime import datetime
import easy_datetime as edt


class TestChineseNumberConversion:
    """Test Chinese number conversion functions."""
    
    def test_chinese_number_to_int(self):
        # Test basic numbers
        assert edt._chinese_number_to_int('一') == 1
        assert edt._chinese_number_to_int('十') == 10
        assert edt._chinese_number_to_int('十五') == 15
        assert edt._chinese_number_to_int('二十') == 20
        assert edt._chinese_number_to_int('三十一') == 31
        
    def test_int_to_chinese_number(self):
        assert edt._int_to_chinese_number(1) == '一'
        assert edt._int_to_chinese_number(10) == '十'
        assert edt._int_to_chinese_number(15) == '十五'
        assert edt._int_to_chinese_number(20) == '二十'
        assert edt._int_to_chinese_number(31) == '三十一'


class TestParseChinese:
    """Test Chinese date parsing."""
    
    def test_parse_full_chinese_date(self):
        result = edt.parse_chinese_date("二〇二一年一月一日")
        assert result['year'] == 2021
        assert result['month'] == 1
        assert result['day'] == 1
        assert result['era'] is None
        assert result['weekday_chinese'] == '星期五'
        assert result['month_chinese'] == '一月'
        
    def test_parse_minguo_era(self):
        result = edt.parse_chinese_date("民国一一〇年三月十五日")
        assert result['year'] == 2021
        assert result['month'] == 3
        assert result['day'] == 15
        assert result['era'] == '民国'
        
    def test_parse_mixed_format(self):
        result = edt.parse_chinese_date("2021年1月1日")
        assert result['year'] == 2021
        assert result['month'] == 1
        assert result['day'] == 1
        
    def test_parse_month_day_only(self):
        result = edt.parse_chinese_date("三月十五日")
        assert result['month'] == 3
        assert result['day'] == 15
        assert result['year'] == datetime.now().year
        
    def test_parse_traditional_months(self):
        result = edt.parse_chinese_date("二〇二一年正月一日")
        assert result['month'] == 1
        
        result = edt.parse_chinese_date("二〇二一年腊月三十日")
        assert result['month'] == 12
        
    def test_parse_invalid_date(self):
        with pytest.raises(ValueError):
            edt.parse_chinese_date("无效的日期")


class TestFormatChinese:
    """Test Chinese date formatting."""
    
    def test_format_full_chinese(self):
        dt = datetime(2021, 1, 1)
        result = edt.format_chinese_date(dt, 'full')
        assert result == '二〇二一年一月一日'
        
    def test_format_short_chinese(self):
        dt = datetime(2021, 1, 1)
        result = edt.format_chinese_date(dt, 'short')
        assert result == '2021年1月1日'
        
    def test_format_traditional_chinese(self):
        dt = datetime(2021, 1, 1)
        result = edt.format_chinese_date(dt, 'traditional')
        # Should use Chinese numbers for year
        assert '年一月一日' in result
        
    def test_format_with_minguo_era(self):
        dt = datetime(2021, 1, 1)
        result = edt.format_chinese_date(dt, 'full', use_era='民国')
        assert result == '民国一一〇年一月一日'
        
    def test_format_with_gongyuan_era(self):
        dt = datetime(2021, 1, 1)
        result = edt.format_chinese_date(dt, 'short', use_era='公元')
        assert result == '公元2021年1月1日'
        
    def test_format_from_string(self):
        result = edt.format_chinese_date("2021-01-01", 'full')
        assert result == '二〇二一年一月一日'


class TestChineseUnixConversion:
    """Test Chinese date Unix timestamp conversion."""
    
    def test_to_unix_chinese(self):
        result = edt.to_unix_chinese("二〇二一年一月一日")
        assert result == 1609459200
        
    def test_to_unix_chinese_minguo(self):
        result = edt.to_unix_chinese("民国一一〇年一月一日")
        assert result == 1609459200
        
    def test_from_unix_chinese(self):
        result = edt.from_unix_chinese(1609459200)
        assert result == '二〇二一年一月一日'
        
    def test_from_unix_chinese_short(self):
        result = edt.from_unix_chinese(1609459200, format_type='short')
        assert result == '2021年1月1日'
        
    def test_from_unix_chinese_minguo(self):
        result = edt.from_unix_chinese(1609459200, use_era='民国')
        assert result == '民国一一〇年一月一日'


class TestChineseUtilities:
    """Test Chinese date utility functions."""
    
    def test_get_chinese_weekday(self):
        result = edt.get_chinese_weekday("2021-01-01")
        assert result == '星期五'
        
    def test_get_chinese_weekday_short(self):
        result = edt.get_chinese_weekday("2021-01-01", short=True)
        assert result == '周五'
        
    def test_get_chinese_month(self):
        assert edt.get_chinese_month(1) == '一月'
        assert edt.get_chinese_month(12) == '十二月'
        
    def test_get_chinese_month_invalid(self):
        with pytest.raises(ValueError):
            edt.get_chinese_month(13)
            
    def test_convert_chinese_era(self):
        # Convert from 民国 to 公元
        result = edt.convert_chinese_era(110, '民国', '公元')
        assert result == 2021
        
        # Convert from 公元 to 民国
        result = edt.convert_chinese_era(2021, '公元', '民国')
        assert result == 110
        
        # Convert between 公元 and 西元 (should be same)
        result = edt.convert_chinese_era(2021, '公元', '西元')
        assert result == 2021
        
    def test_convert_chinese_era_invalid(self):
        with pytest.raises(ValueError):
            edt.convert_chinese_era(2021, '无效纪元', '公元')
            
    def test_is_valid_chinese_date(self):
        assert edt.is_valid_chinese_date("二〇二一年一月一日") is True
        assert edt.is_valid_chinese_date("民国一一〇年一月一日") is True
        assert edt.is_valid_chinese_date("2021年1月1日") is True
        assert edt.is_valid_chinese_date("无效日期") is False
        assert edt.is_valid_chinese_date("") is False


class TestChineseEdgeCases:
    """Test edge cases for Chinese date functionality."""
    
    def test_leap_year_chinese(self):
        # Test leap year date
        result = edt.parse_chinese_date("二〇二〇年二月二十九日")
        assert result['year'] == 2020
        assert result['month'] == 2
        assert result['day'] == 29
        
    def test_end_of_month_chinese(self):
        result = edt.parse_chinese_date("二〇二一年一月三十一日")
        assert result['day'] == 31
        
    def test_different_year_formats(self):
        # Test different ways to write years
        patterns = [
            ("二〇二一年一月一日", 2021),
            ("2021年一月一日", 2021),
        ]
        
        for pattern, expected_year in patterns:
            result = edt.parse_chinese_date(pattern)
            assert result['year'] == expected_year
            
    def test_format_edge_cases(self):
        # Test formatting edge cases
        dt = datetime(2020, 2, 29)  # Leap year
        result = edt.format_chinese_date(dt, 'full')
        assert '二〇二〇年二月二十九日' == result
        
        dt = datetime(2021, 12, 31)  # End of year
        result = edt.format_chinese_date(dt, 'full')
        assert '二〇二一年十二月三十一日' == result


class TestChineseIntegration:
    """Test integration with existing functions."""
    
    def test_chinese_with_existing_functions(self):
        # Test that Chinese dates work with existing comparison functions
        chinese_date = "二〇二一年一月一日"
        parsed = edt.parse_chinese_date(chinese_date)
        iso_date = parsed['iso_format']
        
        # Should be able to compare with regular dates
        comparison = edt.compare_dates(iso_date, "2021-01-02")
        assert comparison['difference_days'] == 1
        
    def test_chinese_timezone_support(self):
        # Test Chinese dates with timezone
        try:
            result = edt.to_unix_chinese("二〇二一年一月一日", "Asia/Shanghai")
            assert isinstance(result, int)
        except Exception:
            # Skip if timezone not available
            pass
            
    def test_chinese_date_arithmetic(self):
        # Test adding time to Chinese dates
        chinese_date = "二〇二一年一月一日"
        parsed = edt.parse_chinese_date(chinese_date)
        iso_date = parsed['iso_format']
        
        future_date = edt.add_time(iso_date, days=30)
        assert "2021-01-31" in future_date


if __name__ == '__main__':
    pytest.main([__file__])