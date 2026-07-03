from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        # Jika ini muncul di Roblox, berarti Vercel sudah benar
        self.wfile.write(json.dumps({"generated_text": "Server berhasil tersambung!"}).encode())
        
