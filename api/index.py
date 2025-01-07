from http.server import BaseHTTPRequestHandler
from openai import OpenAI
import json

# Initialize OpenAI client
client = OpenAI(
    api_key="sk-e275a5c8e0684743bf45ab3ebe79607e",
    base_url="https://api.deepseek.com"
)

def generate_response(message):
    try:
        # Check if it's a greeting
        if message.lower() in ["你是谁？", "你是谁", "who are you?", "who are you", "what are you", "what are you?", "who are u"]:
            return "I'm your virtual writing assistant, do you need help?"
        
        # Call Deepseek API
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You're a very good virtual writer. You only speak English."},
                {"role": "user", "content": message}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error in generate_response: {e}")
        raise e

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
            request_body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(request_body)
            message = data.get('message', '').strip()

            if not message:
                self._send_error('No message provided', 400)
                return

            response_text = generate_response(message)
            self._send_response({'response': response_text})

        except Exception as e:
            print(f"Error in handler: {e}")
            self._send_error(str(e), 500)

    def _send_response(self, data):
        self.send_response(200)
        self._set_headers()
        self.wfile.write(json.dumps(data).encode())

    def _send_error(self, message, status_code):
        self.send_response(status_code)
        self._set_headers()
        self.wfile.write(json.dumps({'error': message}).encode())

    def _set_headers(self):
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers() 