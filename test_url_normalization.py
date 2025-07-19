#!/usr/bin/env python3
"""
Test URL normalization functionality.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from webchecker.utils import normalize_url, validate_url
    
    print("🧪 Testing URL Normalization")
    print("=" * 40)
    
    test_cases = [
        ("example.com", "https://example.com"),
        ("www.example.com", "https://www.example.com"),
        ("https://example.com", "https://example.com"),
        ("http://example.com", "http://example.com"),
        ("  example.com  ", "https://example.com"),
        ("subdomain.example.com", "https://subdomain.example.com"),
    ]
    
    all_passed = True
    
    for input_url, expected in test_cases:
        result = normalize_url(input_url)
        passed = result == expected
        status = "✅ PASS" if passed else "❌ FAIL"
        
        print(f"Input: {repr(input_url)}")
        print(f"Output: {result}")
        print(f"Expected: {expected}")
        print(f"Status: {status}")
        print()
        
        if not passed:
            all_passed = False
    
    print("=" * 40)
    if all_passed:
        print("🎉 All URL normalization tests passed!")
    else:
        print("❌ Some tests failed")
    
    # Test validation
    print("\n🧪 Testing URL Validation")
    print("=" * 40)
    
    validation_tests = [
        ("https://example.com", True),
        ("http://example.com", True),
        ("example.com", False),  # No protocol
        ("not-a-url", False),
        ("", False),
    ]
    
    for test_url, should_be_valid in validation_tests:
        is_valid = validate_url(test_url)
        status = "✅ PASS" if is_valid == should_be_valid else "❌ FAIL"
        
        print(f"URL: {repr(test_url)}")
        print(f"Valid: {is_valid}")
        print(f"Expected: {should_be_valid}")
        print(f"Status: {status}")
        print()
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 