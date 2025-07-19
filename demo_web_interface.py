#!/usr/bin/env python3
"""
Demo script for the WebChecker web interface.
"""

import sys
import os
import time
import webbrowser
import threading

def main():
    """Demo the web interface."""
    print("🌐 WebChecker Web Interface Demo")
    print("=" * 50)
    
    try:
        # Import the web app
        sys.path.insert(0, os.path.dirname(__file__))
        from webchecker.web_app import WebCheckerApp
        from webchecker.utils import find_available_port
        
        print("✅ Web interface loaded successfully")
        print()
        print("🎯 Features to try:")
        print("  1. Enter a website URL (e.g., https://example.com)")
        print("  2. Enter a pattern to search (e.g., @, ™, ©)")
        print("  3. Watch real-time progress updates")
        print("  4. See current page being scraped")
        print("  5. Export results when complete")
        print()
        print("🚀 Starting web server...")
        
        # Find available port
        port = find_available_port(8080, 10)
        if not port:
            print("❌ Error: No available ports found (8080-8089)")
            return 1
        
        # Start the web app in a separate thread
        app = WebCheckerApp()
        
        def start_server():
            app.run(debug=False, host='0.0.0.0', port=port)
        
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        
        # Wait a moment for server to start
        time.sleep(2)
        
        print("✅ Server started successfully!")
        print(f"🌐 Opening browser to http://localhost:{port}")
        print()
        print("💡 Demo suggestions:")
        print("  • Try searching for '@' on a website to find email addresses")
        print("  • Search for '™' to find trademark symbols")
        print("  • Use '©' to find copyright notices")
        print("  • Watch the progress bar update in real-time")
        print("  • Export results when scraping is complete")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Open browser
        try:
            webbrowser.open(f'http://localhost:{port}')
        except:
            print("⚠️  Could not open browser automatically")
            print(f"   Please open http://localhost:{port} manually")
        
        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Demo stopped by user")
            
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("Make sure you have installed the dependencies:")
        print("  poetry install")
        return 1
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 