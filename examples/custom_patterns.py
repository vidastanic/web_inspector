#!/usr/bin/env python3
"""
Example script: Custom pattern matching.

This script demonstrates how to use custom regex patterns to find
various types of content on websites.
"""

import sys
import os

# Add the parent directory to the path so we can import webchecker
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from webchecker.scraper import WebScraper
from webchecker.patterns import PatternMatcher
from webchecker.utils import setup_logging


def main():
    """Example: Find various patterns using custom regex."""
    
    # Setup logging
    logger = setup_logging(verbose=True)
    
    # Configuration
    target_url = "https://example.com"  # Replace with your target URL
    max_pages = 10
    max_depth = 2
    
    logger.info("Starting custom pattern search...")
    
    # Initialize scraper
    scraper = WebScraper(
        max_pages=max_pages,
        max_depth=max_depth,
        timeout=10,
        user_agent="WebChecker-Example/1.0",
        delay=1.0
    )
    
    # Define various patterns to search for
    patterns = {
        "Email Addresses": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "Phone Numbers": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        "Credit Card Numbers": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        "IP Addresses": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        "URLs": r'https?://[^\s<>"{}|\\^`\[\]]+',
        "Dates (MM/DD/YYYY)": r'\b(0?[1-9]|1[012])/(0?[1-9]|[12][0-9]|3[01])/\d{4}\b',
        "Social Security Numbers": r'\b\d{3}-\d{2}-\d{4}\b',
        "Postal Codes": r'\b\d{5}(?:-\d{4})?\b',
    }
    
    try:
        for pattern_name, pattern_regex in patterns.items():
            print(f"\nSearching for {pattern_name}...")
            print("=" * 50)
            
            # Initialize pattern matcher
            pattern_matcher = PatternMatcher(custom_pattern=pattern_regex)
            
            # Perform the scrape
            results = scraper.scrape_site(
                start_url=target_url,
                pattern_matcher=pattern_matcher,
                extract_before=False  # Don't extract context for these patterns
            )
            
            # Display results
            if results:
                print(f"Found {len(results)} {pattern_name.lower()}:")
                for result in results:
                    print(f"  {result}")
            else:
                print(f"No {pattern_name.lower()} found.")
            
            print()
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return 1
    
    finally:
        scraper.close()
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 