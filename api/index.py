from http.server import BaseHTTPRequestHandler
import json
import requests
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        # API Key HuggingFace (Simpan di Environment Variables Vercel)
        HF_TOKEN = os.environ.get("HF_TOKEN")
        
        # Contoh menggunakan model Llama-3 atau model lain di HuggingFace
        model_url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
        
        response = requests.post(
            model_url,
            json={"inputs": data['prompt']},
            headers={"Authorization": f"Bearer {HF_TOKEN}"}
        )
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response.content)
        
