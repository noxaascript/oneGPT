from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Baca data
            content_length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(content_length))
            
            # Request ke HuggingFace
            url = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"
            token = os.environ.get("HF_TOKEN")
            
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
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
            
