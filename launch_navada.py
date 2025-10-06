#!/usr/bin/env python3
"""
NAVADA Quick Launch Script
One-click launch for AI Live Jobs Intelligence Platform
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
import http.server
import socketserver
from datetime import datetime

def start_server(port=8000):
    """Start HTTP server in background"""
    Handler = http.server.SimpleHTTPRequestHandler
    Handler.extensions_map.update({
        '.csv': 'text/csv',
        '.html': 'text/html',
        '.png': 'image/png',
    })

    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Server running at http://localhost:{port}/")
        httpd.serve_forever()

def main():
    """Quick launch NAVADA from AiLiveJobs folder"""

    print("="*70)
    print("NAVADA - AI LIVE JOBS INTELLIGENCE PLATFORM")
    print("="*70)
    print("Advanced UK AI jobs market intelligence with live data")

    # Check if we're in the right directory
    required_files = [
        'navada_dashboard.html',
        'enhanced_navada_launcher.py',
        'real_time_data_fetcher.py',
        '.env'
    ]

    missing_files = [f for f in required_files if not os.path.exists(f)]

    if missing_files:
        print("\nERROR: Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nMake sure you're running this from the AiLiveJobs folder")
        return False

    print("\nAll required files found")

    # Check environment file
    if not os.path.exists('.env'):
        print("\nWARNING: .env file not found")
        print("Please create .env with your API keys:")
        print("   ADZUNA_APP_ID=your_app_id")
        print("   ADZUNA_APP_KEY=your_app_key")
        print("   OPENAI_API_KEY=your_openai_key")
        return False

    # Update data first
    print("\nUpdating live data...")
    try:
        subprocess.run([sys.executable, 'real_time_data_fetcher.py'],
                      capture_output=True, timeout=30)
        print("Live data updated")
    except:
        print("Using existing data")

    # Start HTTP server in background thread
    print("\nStarting local server...")
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Wait for server to start
    time.sleep(2)

    # Open browser
    print("Opening dashboard in browser...")
    webbrowser.open('http://localhost:8000/navada_dashboard.html')

    print("\n" + "="*70)
    print("NAVADA is running!")
    print("Dashboard: http://localhost:8000/navada_dashboard.html")
    print("Press Ctrl+C to stop the server")
    print("="*70)

    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\n\nLaunch cancelled by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        input("Press Enter to exit...")