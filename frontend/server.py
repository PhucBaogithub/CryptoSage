"""Simple HTTP server for serving the frontend."""

import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

class FrontendHandler(SimpleHTTPRequestHandler):
    """Custom handler to serve frontend files."""
    
    def end_headers(self):
        """Add CORS headers."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()
    
    def log_message(self, format, *args):
        """Log messages."""
        print(f"[{self.log_date_time_string()}] {format % args}")


def start_frontend_server(host='0.0.0.0', port=3000):
    """Start the frontend server."""
    # Change to frontend directory
    frontend_dir = Path(__file__).parent
    os.chdir(frontend_dir)
    
    server_address = (host, port)
    httpd = HTTPServer(server_address, FrontendHandler)
    
    print(f"Frontend server running at http://{host}:{port}")
    print(f"Serving files from: {frontend_dir}")
    print("Press Ctrl+C to stop")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        sys.exit(0)


if __name__ == '__main__':
    start_frontend_server()

