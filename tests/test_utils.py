"""
Tests for utility functions.
"""

import pytest
from webchecker.utils import (
    validate_url, clean_text, extract_domain, 
    is_same_domain, sanitize_filename, format_file_size
)


class TestUtils:
    """Test cases for utility functions."""
    
    def test_validate_url_valid(self):
        """Test URL validation with valid URLs."""
        valid_urls = [
            "https://example.com",
            "http://example.com",
            "https://www.example.com/path",
            "http://subdomain.example.com:8080/path?param=value#fragment"
        ]
        
        for url in valid_urls:
            assert validate_url(url) is True
    
    def test_validate_url_invalid(self):
        """Test URL validation with invalid URLs."""
        invalid_urls = [
            "not-a-url",
            "example.com",
            "ftp://example.com",  # Unsupported scheme
            "",
            "https://",
            "http://"
        ]
        
        for url in invalid_urls:
            assert validate_url(url) is False
    
    def test_clean_text(self):
        """Test text cleaning functionality."""
        dirty_text = "  This   has   extra   spaces  \n\nand\n\nnewlines  "
        cleaned = clean_text(dirty_text)
        
        assert cleaned == "This has extra spaces and newlines"
    
    def test_clean_text_html_entities(self):
        """Test cleaning of HTML entities."""
        text_with_entities = "Brand&nbsp;Name&trade;&amp;Company"
        cleaned = clean_text(text_with_entities)
        
        assert "&nbsp;" not in cleaned
        assert "&amp;" not in cleaned
        assert "Brand Name" in cleaned
    
    def test_extract_domain(self):
        """Test domain extraction."""
        assert extract_domain("https://example.com/path") == "example.com"
        assert extract_domain("http://www.example.com") == "www.example.com"
        assert extract_domain("https://sub.example.com:8080") == "sub.example.com"
        assert extract_domain("invalid-url") is None
    
    def test_is_same_domain(self):
        """Test same domain checking."""
        assert is_same_domain("https://example.com", "https://example.com/path") is True
        assert is_same_domain("https://www.example.com", "https://example.com") is False
        assert is_same_domain("https://example.com", "https://other.com") is False
        assert is_same_domain("invalid", "https://example.com") is False
    
    def test_sanitize_filename(self):
        """Test filename sanitization."""
        assert sanitize_filename("file<name>.txt") == "file_name_.txt"
        assert sanitize_filename("file/name.txt") == "file_name.txt"
        assert sanitize_filename("file\\name.txt") == "file_name.txt"
        assert sanitize_filename("file:name.txt") == "file_name.txt"
        assert sanitize_filename("file*name.txt") == "file_name.txt"
        assert sanitize_filename("file?name.txt") == "file_name.txt"
        assert sanitize_filename("file|name.txt") == "file_name.txt"
        assert sanitize_filename("  file.txt  ") == "file.txt"
        assert sanitize_filename("..file.txt") == "file.txt"
    
    def test_format_file_size(self):
        """Test file size formatting."""
        assert format_file_size(0) == "0B"
        assert format_file_size(1024) == "1.0KB"
        assert format_file_size(1024 * 1024) == "1.0MB"
        assert format_file_size(1024 * 1024 * 1024) == "1.0GB"
        assert format_file_size(500) == "500.0B"
        assert format_file_size(1500) == "1.5KB" 