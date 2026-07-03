from http.server import BaseHTTPRequestHandler
import json
import requests
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 1. Ambil data dari request
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            # 2. Ambil token dari environment
            token = os.environ.get("HF_TOKEN")
            
            # 3. Request ke AI
            # Kita gunakan model yang ringan & stabil
            url = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"
            headers = {"Authorization": f"Bearer {token}"}
            payload = {"inputs": data.get("prompt", "Halo")}
            
            response = requests.post(url, headers=headers, json=payload)
            
            # 4. Kirim balik ke Roblox
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response.content)
            
        except Exception as e:
            # Jika error, kirim pesan error ke Roblox agar kita tahu masalahnya
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
            
