from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Baca data dari Roblox
            content_length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(content_length))
            
            # Siapkan token
            token = os.environ.get("HF_TOKEN")
            
            # Siapkan request ke HuggingFace
            url = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            payload = json.dumps({"inputs": data.get("prompt", "Halo")}).encode()
            
            # Kirim request
            req = urllib.request.Request(url, data=payload, headers=headers)
            with urllib.request.urlopen(req) as response:
                result = response.read()
            
            # Balas ke Roblox
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(result)
            
        except Exception as e:
            # Jika Error, kirim error ke Roblox agar kita tahu masalahnya
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
            
