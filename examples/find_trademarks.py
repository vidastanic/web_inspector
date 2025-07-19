#!/usr/bin/env python3
"""
Example script: Find trademark symbols on a website.

This script demonstrates how to use the WebChecker to find trademark symbols
and extract the brand names associated with them.
"""

import sys
import os

# Add the parent directory to the path so we can import webchecker
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from webchecker.scraper import WebScraper
from webchecker.patterns import PatternMatcher
from webchecker.utils import setup_logging


def main():
    """Example: Find trademark symbols on a website."""
    
    # Setup logging
    logger = setup_logging(verbose=True)
    
    # Configuration
    target_url = "https://example.com"  # Replace with your target URL
    max_pages = 20
    max_depth = 2
    
    logger.info("Starting trademark symbol search...")
    
    # Initialize scraper
    scraper = WebScraper(
        max_pages=max_pages,
        max_depth=max_depth,
        timeout=10,
        user_agent="WebChecker-Example/1.0",
        follow_sitemap=True,
        delay=1.0
    )
    
    # Initialize pattern matcher for trademark symbols
    pattern_matcher = PatternMatcher(pattern="™")
    
    try:
        # Perform the scrape
        results = scraper.scrape_site(
            start_url=target_url,
            pattern_matcher=pattern_matcher,
            extract_before=True  # Extract text before the ™ symbol
        )
        
        # Display results
        if results:
            print(f"\nFound {len(results)} trademark symbols:")
            print("=" * 50)
            for result in results:
                print(f"  {result}")
        else:
            print("No trademark symbols found.")
        
        # Also try to find registered trademarks
        print(f"\nSearching for registered trademarks (®)...")
        registered_matcher = PatternMatcher(pattern="®")
        registered_results = scraper.scrape_site(
            start_url=target_url,
            pattern_matcher=registered_matcher,
            extract_before=True
        )
        
        if registered_results:
            print(f"Found {len(registered_results)} registered trademarks:")
            print("=" * 50)
            for result in registered_results:
                print(f"  {result}")
        else:
            print("No registered trademarks found.")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return 1
    
    finally:
        scraper.close()
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 