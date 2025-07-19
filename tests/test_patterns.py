"""
Tests for the PatternMatcher class.
"""

import pytest
from webchecker.patterns import PatternMatcher


class TestPatternMatcher:
    """Test cases for PatternMatcher class."""
    
    def test_basic_pattern_matching(self):
        """Test basic pattern matching functionality."""
        matcher = PatternMatcher(pattern="™")
        text = "This is a test with BrandName™ and AnotherBrand™"
        
        matches = matcher.find_matches(text)
        assert len(matches) == 2
        assert "™" in matches[0]
        assert "™" in matches[1]
    
    def test_extract_before_functionality(self):
        """Test extracting text before the matched pattern."""
        matcher = PatternMatcher(pattern="™")
        text = "This is a test with BrandName™ and AnotherBrand™"
        
        matches = matcher.find_matches(text, extract_before=True)
        assert len(matches) == 2
        assert "BrandName™" in matches
        assert "AnotherBrand™" in matches
    
    def test_custom_pattern_matching(self):
        """Test custom regex pattern matching."""
        matcher = PatternMatcher(custom_pattern=r'\b\w+\s*™\b')
        text = "This is a test with BrandName™ and AnotherBrand™"
        
        matches = matcher.find_matches(text)
        assert len(matches) == 2
        assert "BrandName™" in matches
        assert "AnotherBrand™" in matches
    
    def test_trademark_matches(self):
        """Test specialized trademark matching."""
        matcher = PatternMatcher()
        text = "BrandName™ ProductName® Copyright©"
        
        matches = matcher.find_trademark_matches(text)
        assert len(matches) >= 3  # Should find TM, R, and C symbols
    
    def test_common_symbols(self):
        """Test finding common symbols."""
        matcher = PatternMatcher()
        text = "BrandName™ ProductName® Copyright© 25° $100"
        
        results = matcher.find_common_symbols(text)
        assert 'trademark' in results
        assert 'registered' in results
        assert 'copyright' in results
        assert 'degree' in results
        assert 'currency' in results
    
    def test_no_matches(self):
        """Test behavior when no matches are found."""
        matcher = PatternMatcher(pattern="™")
        text = "This text has no trademark symbols"
        
        matches = matcher.find_matches(text)
        assert len(matches) == 0
    
    def test_empty_text(self):
        """Test behavior with empty text."""
        matcher = PatternMatcher(pattern="™")
        text = ""
        
        matches = matcher.find_matches(text)
        assert len(matches) == 0
    
    def test_invalid_initialization(self):
        """Test that initialization fails without pattern."""
        with pytest.raises(ValueError):
            PatternMatcher()
    
    def test_case_insensitive_matching(self):
        """Test case insensitive matching with custom patterns."""
        matcher = PatternMatcher(custom_pattern=r'\b\w+\s*™\b')
        text = "BRANDNAME™ brandname™ BrandName™"
        
        matches = matcher.find_matches(text)
        assert len(matches) == 3
    
    def test_unicode_support(self):
        """Test Unicode character support."""
        matcher = PatternMatcher(pattern="©")
        text = "Copyright © 2024 Company Name"
        
        matches = matcher.find_matches(text)
        assert len(matches) == 1
        assert "©" in matches[0] 