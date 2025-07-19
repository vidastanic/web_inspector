#!/usr/bin/env python3
"""
Test script to demonstrate improved text extraction with proper boundary detection.
"""

import sys
import os

def test_text_extraction():
    """Test the improved text extraction functionality."""
    
    # Add the current directory to the path
    sys.path.insert(0, os.path.dirname(__file__))
    
    from webchecker.patterns import PatternMatcher
    
    print("🧪 Testing Improved Text Extraction")
    print("=" * 50)
    
    # Test cases with problematic scenarios
    test_cases = [
        {
            "name": "Email at end of line",
            "text": "Contact us at john@example.com.\nNext line content here.",
            "pattern": "@",
            "expected": "john@example.com"
        },
        {
            "name": "Email with trailing comma",
            "text": "Email: jane@company.com, phone: 123-456-7890",
            "pattern": "@",
            "expected": "jane@company.com"
        },
        {
            "name": "Email with HTML tags",
            "text": "Contact: <a href='mailto:info@site.com'>info@site.com</a>",
            "pattern": "@",
            "expected": "info@site.com"
        },
        {
            "name": "Trademark symbol",
            "text": "Our product™ is amazing. Next sentence here.",
            "pattern": "™",
            "expected": "product™"
        },
        {
            "name": "Multiple emails in paragraph",
            "text": "Email us at contact@example.com or support@example.com for help.",
            "pattern": "@",
            "expected": ["contact@example.com", "support@example.com"]
        },
        {
            "name": "Email with parentheses",
            "text": "Email: (main) admin@site.com or (support) help@site.com",
            "pattern": "@",
            "expected": ["admin@site.com", "help@site.com"]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   Text: {repr(test_case['text'])}")
        print(f"   Pattern: {test_case['pattern']}")
        
        # Create pattern matcher
        matcher = PatternMatcher(pattern=test_case['pattern'])
        
        # Test extraction with both before and after context
        results = matcher.find_matches(test_case['text'], extract_before=True, extract_after=True)
        
        print(f"   Results: {results}")
        print(f"   Expected: {test_case['expected']}")
        
        # Check if results match expected
        if isinstance(test_case['expected'], list):
            success = len(results) == len(test_case['expected']) and all(r in test_case['expected'] for r in results)
        else:
            success = len(results) == 1 and results[0] == test_case['expected']
        
        if success:
            print("   ✅ PASS")
        else:
            print("   ❌ FAIL")
    
    print("\n" + "=" * 50)
    print("🎯 Key Improvements:")
    print("   • Respects line breaks and paragraph boundaries")
    print("   • Stops at punctuation marks (.,;:!?)")
    print("   • Removes trailing punctuation from results")
    print("   • Handles HTML-like characters and control characters")
    print("   • More precise word boundary detection")

if __name__ == "__main__":
    test_text_extraction() 