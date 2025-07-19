#!/usr/bin/env python3
"""
Simple test for the text extraction fix.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from webchecker.patterns import PatternMatcher
    
    print("🧪 Testing Fixed Text Extraction")
    print("=" * 40)
    
    # Test email extraction
    matcher = PatternMatcher('@')
    
    test_text = "Contact us at john@example.com.\nNext line content here."
    results = matcher.find_matches(test_text, extract_before=True, extract_after=True)
    
    print(f"Input: {repr(test_text)}")
    print(f"Results: {results}")
    print(f"Expected: ['john@example.com']")
    
    if results == ['john@example.com']:
        print("✅ PASS - Email extraction fixed!")
    else:
        print("❌ FAIL - Still not working correctly")
    
    # Test multiple emails
    test_text2 = "Email us at contact@example.com or support@example.com for help."
    results2 = matcher.find_matches(test_text2, extract_before=True, extract_after=True)
    
    print(f"\nInput: {repr(test_text2)}")
    print(f"Results: {results2}")
    print(f"Expected: ['contact@example.com', 'support@example.com']")
    
    if results2 == ['contact@example.com', 'support@example.com']:
        print("✅ PASS - Multiple emails extraction fixed!")
    else:
        print("❌ FAIL - Multiple emails still not working")
    
    print("\n" + "=" * 40)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}") 