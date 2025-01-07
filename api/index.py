from openai import OpenAI
import json
from http.server import BaseHTTPRequestHandler

client = OpenAI(
    api_key="sk-e275a5c8e0684743bf45ab3ebe79607e",
    base_url="https://api.deepseek.com/v1"
)

def generate_response(message):
    if message.lower() in ["你是谁？", "你是谁", "who are you?", "who are you", "what are you", "what are you?", "who are u"]:
        return "I'm your virtual writing assistant, do you need help?"
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You're a very good virtual writer. You only speak English."},
            {"role": "user", "content": message}
        ],
        temperature=0.7,
        stream=False
    )
    return response.choices[0].message.content

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            message = data.get('message', '').strip()

            if not message:
                self._send_response(400, {'error': 'No message provided'})
                return

            response_text = generate_response(message)
            self._send_response(200, {'response': response_text})

        except Exception as e:
            print(f"Error: {str(e)}")
            self._send_response(500, {'error': str(e)})

    def do_OPTIONS(self):
        self._set_headers()
        self.send_response(204)
        self.end_headers()

    def _set_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', 'application/json')

    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self._set_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8')) 