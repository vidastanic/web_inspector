#!/usr/bin/env python3
"""
Test script for the WebChecker web interface.
"""

import sys
import os
import time
import requests
import threading

def test_web_interface():
    """Test the web interface functionality."""
    print("🧪 Testing WebChecker Web Interface")
    print("=" * 50)
    
    try:
        # Import the web app
        sys.path.insert(0, os.path.dirname(__file__))
        from webchecker.web_app import WebCheckerApp
        from webchecker.utils import find_available_port
        
        print("✅ Web interface imported successfully")
        
        # Find available port
        port = find_available_port(8080, 10)
        if not port:
            print("❌ Error: No available ports found")
            return False
        
        print(f"🔌 Using port: {port}")
        
        # Start the web app in a separate thread
        app = WebCheckerApp()
        
        def start_server():
            app.run(debug=False, host='0.0.0.0', port=port)
        
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(3)
        
        # Test the main page
        try:
            response = requests.get(f'http://localhost:{port}/', timeout=5)
            if response.status_code == 200:
                print("✅ Main page loads successfully")
            else:
                print(f"❌ Main page returned status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Could not connect to web server: {e}")
            return False
        
        # Test the API endpoint
        try:
            response = requests.post(
                f'http://localhost:{port}/api/start-scrape',
                json={
                    'url': 'https://example.com',
                    'pattern': '@',
                    'max_pages': 1,
                    'max_depth': 1,
                    'follow_sitemap': False
                },
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                if 'session_id' in data:
                    print("✅ API endpoint responds correctly")
                    session_id = data['session_id']
                    
                    # Test status endpoint
                    time.sleep(1)
                    status_response = requests.get(f'http://localhost:{port}/api/status/{session_id}', timeout=5)
                    if status_response.status_code == 200:
                        print("✅ Status endpoint works")
                    else:
                        print(f"❌ Status endpoint returned: {status_response.status_code}")
                        
                else:
                    print("❌ API response missing session_id")
                    return False
            else:
                print(f"❌ API endpoint returned status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ API test failed: {e}")
            return False
        
        print("🎉 All tests passed!")
        print(f"🌐 Web interface is running at: http://localhost:{port}")
        print("=" * 50)
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you have installed the dependencies:")
        print("  poetry install")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_web_interface()
    sys.exit(0 if success else 1) 