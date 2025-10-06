from http.server import BaseHTTPRequestHandler
import json
import os
import csv
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Serve the main dashboard
        if path == '/' or path == '/navada_dashboard.html':
            self.serve_dashboard()
        # Serve job data
        elif path == '/api/jobs':
            self.serve_jobs_data()
        # Serve static files
        elif path.endswith('.css'):
            self.serve_static_file(path, 'text/css')
        elif path.endswith('.js'):
            self.serve_static_file(path, 'application/javascript')
        elif path.endswith('.png'):
            self.serve_static_file(path, 'image/png')
        elif path.endswith('.csv'):
            self.serve_static_file(path, 'text/csv')
        else:
            self.send_error(404, "File not found")

    def serve_dashboard(self):
        try:
            dashboard_path = os.path.join(os.path.dirname(__file__), '..', 'navada_dashboard.html')
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "Dashboard not found")

    def serve_jobs_data(self):
        try:
            csv_path = os.path.join(os.path.dirname(__file__), '..', 'live_uk_ai_jobs.csv')
            jobs = []

            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    jobs.append(row)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(jobs).encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "Jobs data not found")
        except Exception as e:
            self.send_error(500, f"Error reading jobs data: {str(e)}")

    def serve_static_file(self, path, content_type):
        try:
            file_path = os.path.join(os.path.dirname(__file__), '..', path.lstrip('/'))

            if content_type.startswith('image/'):
                with open(file_path, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, f"File not found: {path}")
        except Exception as e:
            self.send_error(500, f"Error serving file: {str(e)}")