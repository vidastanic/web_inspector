#!/usr/bin/env python3
"""
Web server launcher for WebChecker.
"""

import sys
import os
import time
import webbrowser
import threading

def main():
    """Launch the web server."""
    try:
        # Add the current directory to the path
        sys.path.insert(0, os.path.dirname(__file__))
        
        # Import the web app components
        from webchecker.web_app import WebCheckerApp
        from webchecker.utils import find_available_port
        
        print("🌐 WebChecker Web Interface")
        print("=" * 50)
        print("Starting web server...")
        
        # Find available port
        port = find_available_port(8080, 10)
        if not port:
            print("❌ Error: No available ports found (8080-8089)")
            return 1
        
        print(f"Open your browser and go to: http://localhost:{port}")
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Create and start the web app
        app = WebCheckerApp()
        
        def start_server():
            app.run(debug=False, host='0.0.0.0', port=port)
        
        # Start server in background thread
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        
        # Wait a moment for server to start
        time.sleep(2)
        
        # Open browser automatically
        try:
            print(f"🌐 Opening browser to http://localhost:{port}")
            webbrowser.open(f'http://localhost:{port}')
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print(f"   Please open http://localhost:{port} manually")
        
        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Server stopped by user")
            return 0
        
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("Make sure you have installed the dependencies:")
        print("  poetry install")
        return 1
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 