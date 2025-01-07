from http.server import BaseHTTPRequestHandler
import json
from openai import OpenAI
import os

# Initialize OpenAI client with Deepseek configuration
client = OpenAI(
    api_key="sk-e275a5c8e0684743bf45ab3ebe79607e",
    base_url="https://api.deepseek.com/v1"
)

GREETING_QUESTIONS = [
    "你是谁？",
    "你是谁",
    "who are you?",
    "who are you",
    "what are you",
    "what are you?",
    "who are u"
]

def handle_chat(message):
    try:
        if not message:
            return {'error': 'No message provided'}, 400

        # Check if it's a greeting question
        if message.lower() in GREETING_QUESTIONS:
            return {'response': "I'm your virtual writing assistant, do you need help?"}, 200

        # Call Deepseek API using OpenAI SDK
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You're a very good virtual writer. You only speak English."},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            stream=False
        )
        
        return {'response': response.choices[0].message.content}, 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return {'error': f'Server Error: {str(e)}'}, 500

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)
            message = data.get('message', '').strip()
            
            response, status_code = handle_chat(message)
            
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {'error': str(e)}
            self.wfile.write(json.dumps(error_response).encode()) 