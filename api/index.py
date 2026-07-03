from http.server import BaseHTTPRequestHandler
import json
import requests
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        # Token diambil dari Environment Variable
        token = os.environ.get("HF_TOKEN")
        
        # Panggil HuggingFace
        url = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"inputs": data.get("prompt", "Halo")}
        
        resp = requests.post(url, headers=headers, json=payload)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(resp.content)
        
