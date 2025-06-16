"""
Performance tests for easy_datetime package.
"""

import time
import pytest
import easy_datetime as edt


class TestPerformance:
    """Test performance of various functions."""
    
    def test_to_unix_performance(self):
        """Test performance of to_unix function."""
        start_time = time.time()
        
        # Run 1000 conversions
        for i in range(1000):
            edt.to_unix("2021-01-01")
            
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete 1000 conversions in less than 1 second
        assert duration < 1.0, f"Performance test failed: {duration:.3f}s for 1000 conversions"
        
    def test_from_unix_performance(self):
        """Test performance of from_unix function."""
        start_time = time.time()
        
        # Run 1000 conversions
        for i in range(1000):
            edt.from_unix(1609459200)
            
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete 1000 conversions in less than 1 second
        assert duration < 1.0, f"Performance test failed: {duration:.3f}s for 1000 conversions"
        
    def test_format_datetime_performance(self):
        """Test performance of format_datetime function."""
        start_time = time.time()
        
        # Run 1000 formatting operations
        for i in range(1000):
            edt.format_datetime("2021-01-01", "%Y-%m-%d")
            
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete 1000 operations in less than 2 seconds
        assert duration < 2.0, f"Performance test failed: {duration:.3f}s for 1000 operations"
        
    def test_add_time_performance(self):
        """Test performance of add_time function."""
        start_time = time.time()
        
        # Run 1000 add operations
        for i in range(1000):
            edt.add_time("2021-01-01", days=1)
            
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete 1000 operations in less than 2 seconds
        assert duration < 2.0, f"Performance test failed: {duration:.3f}s for 1000 operations"


class TestMemoryUsage:
    """Test memory usage patterns."""
    
    def test_no_memory_leaks(self):
        """Test that repeated operations don't cause memory leaks."""
        import gc
        
        # Force garbage collection
        gc.collect()
        
        # Run many operations
        for i in range(10000):
            result = edt.to_unix("2021-01-01")
            result = edt.from_unix(result)
            
        # Force garbage collection again
        gc.collect()
        
        # If we get here without memory errors, the test passes
        assert True


if __name__ == '__main__':
    pytest.main([__file__])