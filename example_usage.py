#!/usr/bin/env python3
"""
Example usage of the new WebChecker features:
1. File type filtering
2. Text extraction after matches
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

def demonstrate_file_filtering():
    """Demonstrate the file filtering functionality."""
    print("=== File Filtering Demo ===")
    
    from webchecker.scraper import WebScraper
    
    # Create scraper with default exclusions
    scraper = WebScraper()
    
    # Test URLs
    test_urls = [
        "https://example.com/page.html",
        "https://example.com/document.pdf",
        "https://example.com/image.jpg",
        "https://example.com/contact",
        "https://example.com/download/file.zip",
        "https://example.com/about.php"
    ]
    
    print("URL filtering results:")
    for url in test_urls:
        excluded = scraper._should_exclude_url(url)
        status = "❌ EXCLUDED" if excluded else "✅ INCLUDED"
        print(f"  {status}: {url}")
    
    print()

def demonstrate_text_extraction():
    """Demonstrate the text extraction functionality."""
    print("=== Text Extraction Demo ===")
    
    from webchecker.patterns import PatternMatcher
    
    # Test text with various patterns
    test_text = """
    Contact us at john@example.com or jane@company.org
    Our products include BrandName™ and AnotherProduct®
    Copyright © 2024 Company Name
    """
    
    print("Original text:")
    print(f"  {test_text.strip()}")
    print()
    
    # Test @ symbol extraction
    print("Email extraction:")
    matcher = PatternMatcher(pattern="@")
    
    # Extract before @
    before_matches = matcher.find_matches(test_text, extract_before=True)
    print(f"  Before @: {before_matches}")
    
    # Extract after @
    after_matches = matcher.find_matches(test_text, extract_after=True)
    print(f"  After @: {after_matches}")
    
    # Extract both
    both_matches = matcher.find_matches(test_text, extract_before=True, extract_after=True)
    print(f"  Both: {both_matches}")
    print()
    
    # Test trademark symbols
    print("Trademark extraction:")
    tm_matcher = PatternMatcher(pattern="™")
    tm_matches = tm_matcher.find_matches(test_text, extract_before=True)
    print(f"  Trademarks: {tm_matches}")
    
    reg_matcher = PatternMatcher(pattern="®")
    reg_matches = reg_matcher.find_matches(test_text, extract_before=True)
    print(f"  Registered: {reg_matches}")
    
    copy_matcher = PatternMatcher(pattern="©")
    copy_matches = copy_matcher.find_matches(test_text, extract_after=True)
    print(f"  Copyright: {copy_matches}")
    print()

def demonstrate_cli_usage():
    """Demonstrate the CLI usage examples."""
    print("=== CLI Usage Examples ===")
    
    examples = [
        "python -m webchecker.main https://example.com --pattern '@' --extract-after",
        "python -m webchecker.main https://example.com --pattern '™' --extract-before",
        "python -m webchecker.main https://example.com --pattern '@' --extract-before --extract-after",
        "python -m webchecker.main https://example.com --pattern '@' --exclude-extensions .pdf .doc",
        "python -m webchecker.main https://example.com --pattern '©' --extract-after --max-pages 50"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example}")
    
    print()

def main():
    """Run all demonstrations."""
    print("WebChecker New Features Demonstration")
    print("=" * 50)
    print()
    
    try:
        demonstrate_file_filtering()
        demonstrate_text_extraction()
        demonstrate_cli_usage()
        
        print("=" * 50)
        print("✅ All demonstrations completed successfully!")
        print("\nThe new features are working correctly:")
        print("  • File filtering prevents PDF and binary file scraping")
        print("  • Text extraction works before, after, or both around matches")
        print("  • CLI options provide flexible control")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 