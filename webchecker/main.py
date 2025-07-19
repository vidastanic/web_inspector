#!/usr/bin/env python3
"""
Main entry point for the WebChecker application.
"""

import argparse
import sys
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import re

from .scraper import WebScraper
from .patterns import PatternMatcher
from .utils import setup_logging, validate_url


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="WebChecker - Find specific characters and patterns on websites",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m webchecker.main https://example.com --pattern "™" --extract-before
  python -m webchecker.main https://example.com --pattern "®" --extract-before --max-pages 10
  python -m webchecker.main https://example.com --custom-pattern "\\b\\w+\\s*™\\b" --verbose
  python -m webchecker.main https://example.com --pattern "@" --extract-after
  python -m webchecker.main https://example.com --pattern "™" --extract-before --extract-after
  python -m webchecker.main https://example.com --pattern "@" --exclude-extensions .pdf .doc
        """
    )
    
    parser.add_argument(
        "url",
        help="The starting URL to scrape"
    )
    
    parser.add_argument(
        "--pattern",
        help="Unicode character or string to search for (e.g., '™', '®', '©')"
    )
    
    parser.add_argument(
        "--custom-pattern",
        help="Custom regex pattern to search for"
    )
    
    parser.add_argument(
        "--extract-before",
        action="store_true",
        help="Extract text before the matched pattern (up to the previous space)"
    )
    
    parser.add_argument(
        "--extract-after",
        action="store_true",
        help="Extract text after the matched pattern (up to the next space)"
    )
    
    parser.add_argument(
        "--exclude-extensions",
        nargs="+",
        default=None,
        help="File extensions to exclude (e.g., .pdf .doc .zip). Default excludes common binary files."
    )
    
    parser.add_argument(
        "--max-pages",
        type=int,
        default=50,
        help="Maximum number of pages to scrape (default: 50)"
    )
    
    parser.add_argument(
        "--max-depth",
        type=int,
        default=3,
        help="Maximum depth to follow links (default: 3)"
    )
    
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Request timeout in seconds (default: 10)"
    )
    
    parser.add_argument(
        "--user-agent",
        default="WebChecker/0.1.0",
        help="User agent string for requests"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--output",
        help="Output file for results (default: print to stdout)"
    )
    
    parser.add_argument(
        "--follow-sitemap",
        action="store_true",
        help="Try to discover and follow sitemap.xml"
    )
    
    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logging(verbose=args.verbose)
    
    # Validate URL
    if not validate_url(args.url):
        logger.error(f"Invalid URL: {args.url}")
        sys.exit(1)
    
    # Initialize scraper
    scraper = WebScraper(
        max_pages=args.max_pages,
        max_depth=args.max_depth,
        timeout=args.timeout,
        user_agent=args.user_agent,
        follow_sitemap=args.follow_sitemap,
        exclude_extensions=args.exclude_extensions
    )
    
    # Initialize pattern matcher
    if args.custom_pattern:
        pattern_matcher = PatternMatcher(custom_pattern=args.custom_pattern)
    elif args.pattern:
        pattern_matcher = PatternMatcher(pattern=args.pattern)
    else:
        logger.error("Either --pattern or --custom-pattern must be specified")
        sys.exit(1)
    
    try:
        logger.info(f"Starting scrape of {args.url}")
        logger.info(f"Pattern: {pattern_matcher.pattern}")
        logger.info(f"Max pages: {args.max_pages}, Max depth: {args.max_depth}")
        
        # Perform the scrape
        results = scraper.scrape_site(
            start_url=args.url,
            pattern_matcher=pattern_matcher,
            extract_before=args.extract_before,
            extract_after=args.extract_after
        )
        
        # Output results
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                for result in results:
                    f.write(f"{result}\n")
            logger.info(f"Results saved to {args.output}")
        else:
            for result in results:
                print(result)
        
        logger.info(f"Scraping completed. Found {len(results)} matches.")
        
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 