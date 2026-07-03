from http.server import BaseHTTPRequestHandler
import json
import requests
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Baca body
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        # Ambil Token dari Environment Variable
        HF_TOKEN = os.environ.get("HF_TOKEN")
        
        # Tentukan Model
        model_name = data.get("model", "ultra")
        url = "https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct" if model_name == "flash" else "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
        
        # Request ke HuggingFace
        response = requests.post(
            url,
            json={"inputs": data['prompt']},
            headers={"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
        )
        
        # Kirim balik ke Roblox
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response.content)
        
