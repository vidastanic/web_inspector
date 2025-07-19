#!/usr/bin/env python3
"""
Debug test for text extraction.
"""

print("Starting debug test...")

try:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    
    print("Importing PatternMatcher...")
    from webchecker.patterns import PatternMatcher
    
    print("Creating matcher...")
    matcher = PatternMatcher('@')
    
    print("Testing extraction...")
    test_text = "Contact us at john@example.com.\nNext line content here."
    results = matcher.find_matches(test_text, extract_before=True, extract_after=True)
    
    print(f"Input: {test_text}")
    print(f"Results: {results}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc() 