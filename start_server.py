#!/usr/bin/env python3
"""
Simple HTTP server to serve NAVADA dashboard locally
This avoids CORS issues when loading CSV files
"""

import http.server
import socketserver
import os
import webbrowser
from threading import Timer

PORT = 8888
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Add CORS headers to allow loading local resources
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def log_message(self, format, *args):
        # Suppress standard logging for cleaner output
        pass

def open_browser():
    """Open the dashboard in the default browser"""
    webbrowser.open(f'http://localhost:{PORT}/navada_dashboard.html')

def main():
    print("="*60)
    print("NAVADA SERVER - AI Jobs Intelligence Platform")
    print("="*60)

    os.chdir(DIRECTORY)

    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"[SUCCESS] Server running at http://localhost:{PORT}")
        print(f"[INFO] Serving files from: {DIRECTORY}")
        print(f"[URL] Dashboard: http://localhost:{PORT}/navada_dashboard.html")
        print("\nAvailable resources:")
        print(f"   - Dashboard: http://localhost:{PORT}/navada_dashboard.html")
        print(f"   - Job Data: http://localhost:{PORT}/live_uk_ai_jobs.csv")
        print("\n[ACTION] Opening dashboard in your browser...")
        print("\nPress Ctrl+C to stop the server")
        print("-"*60)

        # Open browser after 1 second
        Timer(1.0, open_browser).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n[STOP] Server stopped")
            print("Thank you for using NAVADA!")

if __name__ == "__main__":
    main()