from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 1. Cek Token
            token = os.environ.get("HF_TOKEN")
            if not token:
                raise Exception("HF_TOKEN di Vercel tidak terdeteksi!")

            # 2. Baca Input
            content_length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(content_length))
            
            # 3. Request ke HuggingFace
            url = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"
            req = urllib.request.Request(
                url, 
                data=json.dumps({"inputs": data.get("prompt", "Halo")}).encode(),
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            )
            
            with urllib.request.urlopen(req) as response:
                result = response.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(result)
            
        except Exception as e:
            # Mengirim pesan error spesifik ke Roblox
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Error pada server: " + str(e)}).encode())
            
