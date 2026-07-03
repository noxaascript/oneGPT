from http.server import BaseHTTPRequestHandler
import json
import requests
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            HF_TOKEN = os.environ.get("HF_TOKEN")
            if not HF_TOKEN:
                raise Exception("HF_TOKEN belum di-set di Vercel!")
                
            model_name = data.get("model", "ultra")
            url = "https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct" if model_name == "flash" else "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
            
            response = requests.post(
                url,
                json={"inputs": data.get('prompt', '')},
                headers={"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
            )
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response.content)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
            
