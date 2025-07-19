"""
Flask web application for WebChecker frontend.
"""

import os
import json
import threading
import time
from typing import Dict, List, Any
from flask import Flask, render_template, request, jsonify, session
from urllib.parse import urlparse

from .scraper import WebScraper
from .patterns import PatternMatcher
from .utils import setup_logging, validate_url, normalize_url, find_available_port


class WebCheckerApp:
    """Main web application class for WebChecker."""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = os.urandom(24)
        self.app.config['SECRET_KEY'] = os.urandom(24)
        
        # Store active scraping sessions
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        
        # Setup logging
        self.logger = setup_logging(verbose=True)
        
        # Register routes
        self._register_routes()
    
    def _register_routes(self):
        """Register Flask routes."""
        
        @self.app.route('/')
        def index():
            """Main page."""
            return render_template('index.html')
        
        @self.app.route('/api/start-scrape', methods=['POST'])
        def start_scrape():
            """Start a new scraping session."""
            try:
                data = request.get_json()
                url = data.get('url', '').strip()
                pattern = data.get('pattern', '').strip()
                max_pages = int(data.get('max_pages', 50))
                max_depth = int(data.get('max_depth', 3))
                follow_sitemap = data.get('follow_sitemap', True)
                
                # Validate inputs
                if not url or not pattern:
                    return jsonify({'error': 'URL and pattern are required'}), 400
                
                # Normalize URL (add protocol if missing)
                url = normalize_url(url)
                
                if not validate_url(url):
                    return jsonify({'error': 'Invalid URL format'}), 400
                
                # Generate session ID
                session_id = f"scrape_{int(time.time())}_{threading.get_ident()}"
                
                # Initialize scraper
                scraper = WebScraper(
                    max_pages=max_pages,
                    max_depth=max_depth,
                    timeout=10,
                    user_agent="WebChecker-Web/1.0",
                    follow_sitemap=follow_sitemap,
                    delay=0.5  # Faster for web interface
                )
                
                # Initialize pattern matcher
                pattern_matcher = PatternMatcher(pattern=pattern)
                
                # Store session info
                self.active_sessions[session_id] = {
                    'scraper': scraper,
                    'pattern_matcher': pattern_matcher,
                    'url': url,
                    'pattern': pattern,
                    'max_pages': max_pages,
                    'status': 'starting',
                    'progress': 0,
                    'current_page': '',
                    'results': [],
                    'total_pages': 0,
                    'start_time': time.time(),
                    'error': None
                }
                
                # Start scraping in background thread
                thread = threading.Thread(
                    target=self._scrape_worker,
                    args=(session_id, url, pattern_matcher, max_pages, max_depth, follow_sitemap)
                )
                thread.daemon = True
                thread.start()
                
                return jsonify({
                    'session_id': session_id,
                    'status': 'started',
                    'message': 'Scraping started successfully'
                })
                
            except Exception as e:
                self.logger.error(f"Error starting scrape: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/status/<session_id>')
        def get_status(session_id):
            """Get scraping status and results."""
            if session_id not in self.active_sessions:
                return jsonify({'error': 'Session not found'}), 404
            
            session_data = self.active_sessions[session_id]
            
            return jsonify({
                'status': session_data['status'],
                'progress': session_data['progress'],
                'current_page': session_data['current_page'],
                'results': session_data['results'],
                'total_pages': session_data['total_pages'],
                'error': session_data['error'],
                'elapsed_time': time.time() - session_data['start_time']
            })
        
        @self.app.route('/api/stop/<session_id>')
        def stop_scrape(session_id):
            """Stop a scraping session."""
            if session_id not in self.active_sessions:
                return jsonify({'error': 'Session not found'}), 404
            
            session_data = self.active_sessions[session_id]
            session_data['status'] = 'stopped'
            session_data['scraper'].close()
            
            return jsonify({'status': 'stopped'})
        
        @self.app.route('/api/clear/<session_id>')
        def clear_session(session_id):
            """Clear a session."""
            if session_id in self.active_sessions:
                session_data = self.active_sessions[session_id]
                session_data['scraper'].close()
                del self.active_sessions[session_id]
            
            return jsonify({'status': 'cleared'})
    
    def _scrape_worker(self, session_id: str, url: str, pattern_matcher: PatternMatcher, 
                      max_pages: int, max_depth: int, follow_sitemap: bool):
        """Background worker for scraping."""
        session_data = self.active_sessions[session_id]
        scraper = session_data['scraper']
        
        try:
            session_data['status'] = 'running'
            
            # Custom scraper that reports progress
            results = self._scrape_with_progress(
                scraper, url, pattern_matcher, session_id, max_pages, max_depth, follow_sitemap
            )
            
            session_data['results'] = results
            session_data['status'] = 'completed'
            session_data['progress'] = 100
            
        except Exception as e:
            self.logger.error(f"Error in scraping worker: {e}")
            session_data['error'] = str(e)
            session_data['status'] = 'error'
        
        finally:
            scraper.close()
    
    def _scrape_with_progress(self, scraper: WebScraper, start_url: str, 
                            pattern_matcher: PatternMatcher, session_id: str,
                            max_pages: int, max_depth: int, follow_sitemap: bool) -> List[str]:
        """Scrape with progress reporting."""
        results = []
        base_domain = urlparse(start_url).netloc
        
        # Initialize URL queue
        url_queue = []
        visited_urls = set()
        
        # Add starting URL
        url_queue.append((start_url, 0))
        
        # Add sitemap URLs if requested
        if follow_sitemap:
            sitemap_urls = scraper._discover_sitemap_urls(start_url)
            for url in sitemap_urls:
                if url not in visited_urls:
                    url_queue.append((url, 0))
        
        # Update total pages
        session_data = self.active_sessions[session_id]
        session_data['total_pages'] = min(len(url_queue), max_pages)
        
        processed_pages = 0
        
        while url_queue and processed_pages < max_pages:
            current_url, depth = url_queue.pop(0)
            
            if current_url in visited_urls or depth > max_depth:
                continue
            
            visited_urls.add(current_url)
            processed_pages += 1
            
            # Update progress
            session_data['current_page'] = current_url
            session_data['progress'] = int((processed_pages / max_pages) * 100)
            
            try:
                # Scrape the page with both extract_before and extract_after
                page_results = scraper._scrape_page(
                    current_url, pattern_matcher, extract_before=True, extract_after=True
                )
                results.extend(page_results)
                
                # Add delay
                time.sleep(scraper.delay)
                
                # Find new links if we haven't reached max depth
                if depth < max_depth:
                    new_links = scraper._extract_links(current_url, base_domain)
                    for link in new_links:
                        if link not in visited_urls:
                            url_queue.append((link, depth + 1))
                
            except Exception as e:
                self.logger.warning(f"Error scraping {current_url}: {e}")
                continue
        
        return results
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Run the Flask application."""
        self.app.run(host=host, port=port, debug=debug)


def create_app():
    """Create and return the Flask application."""
    app_instance = WebCheckerApp()
    return app_instance.app


def main():
    """Main entry point for the web application."""
    app = WebCheckerApp()
    
    # Find available port
    port = find_available_port(8080, 10)
    if not port:
        print("❌ Error: No available ports found (8080-8089)")
        return 1
    
    print("🌐 WebChecker Web Interface")
    print("=" * 40)
    print("Starting web server...")
    print(f"Open your browser and go to: http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    print("=" * 40)
    
    # Open browser automatically
    import webbrowser
    import time
    time.sleep(1)  # Give server a moment to start
    try:
        webbrowser.open(f'http://localhost:{port}')
    except:
        pass  # Silently fail if browser can't be opened
    
    app.run(debug=False, host='0.0.0.0', port=port)


if __name__ == '__main__':
    main() 