from http.server import BaseHTTPRequestHandler
import json
import requests
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        # API Key tersimpan di Environment Variables Vercel
        API_KEY = os.environ.get("DEEPSEEK_KEY")
        
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            json=data,
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        )
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response.content)
      
