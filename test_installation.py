#!/usr/bin/env python3
"""
Test script to verify that the WebChecker installation works correctly.
"""

import sys
import traceback


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from webchecker import __version__, __author__
        print(f"✓ Package imported successfully (version: {__version__})")
    except ImportError as e:
        print(f"✗ Failed to import webchecker package: {e}")
        return False
    
    try:
        from webchecker.scraper import WebScraper
        print("✓ WebScraper imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import WebScraper: {e}")
        return False
    
    try:
        from webchecker.patterns import PatternMatcher
        print("✓ PatternMatcher imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import PatternMatcher: {e}")
        return False
    
    try:
        from webchecker.utils import setup_logging, validate_url
        print("✓ Utils imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import utils: {e}")
        return False
    
    return True


def test_basic_functionality():
    """Test basic functionality without making network requests."""
    print("\nTesting basic functionality...")
    
    try:
        from webchecker.patterns import PatternMatcher
        from webchecker.utils import validate_url, clean_text
        
        # Test pattern matching
        matcher = PatternMatcher(pattern="™")
        text = "This is a test with BrandName™"
        matches = matcher.find_matches(text, extract_before=True)
        
        if matches and "BrandName™" in matches[0]:
            print("✓ Pattern matching works correctly")
        else:
            print("✗ Pattern matching failed")
            return False
        
        # Test URL validation
        if validate_url("https://example.com"):
            print("✓ URL validation works correctly")
        else:
            print("✗ URL validation failed")
            return False
        
        # Test text cleaning
        dirty_text = "  This   has   extra   spaces  "
        cleaned = clean_text(dirty_text)
        if cleaned == "This has extra spaces":
            print("✓ Text cleaning works correctly")
        else:
            print("✗ Text cleaning failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        traceback.print_exc()
        return False


def test_scraper_initialization():
    """Test that the scraper can be initialized."""
    print("\nTesting scraper initialization...")
    
    try:
        from webchecker.scraper import WebScraper
        
        scraper = WebScraper(
            max_pages=10,
            max_depth=2,
            timeout=5,
            user_agent="Test/1.0"
        )
        
        print("✓ Scraper initialized successfully")
        
        # Test that the scraper can be closed
        scraper.close()
        print("✓ Scraper closed successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Scraper initialization failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("WebChecker Installation Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_basic_functionality,
        test_scraper_initialization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! WebChecker is ready to use.")
        print("\nTry running:")
        print("  python -m webchecker.main https://example.com --pattern '™' --extract-before")
        return 0
    else:
        print("❌ Some tests failed. Please check the installation.")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 