from http.server import BaseHTTPRequestHandler
import openai
import json

openai.api_key = "sk-e275a5c8e0684743bf45ab3ebe79607e"
openai.api_base = "https://api.deepseek.com/v1"

def generate_response(message):
    # Check if it's a greeting
    if message.lower() in ["你是谁？", "你是谁", "who are you?", "who are you", "what are you", "what are you?", "who are u"]:
        return "I'm your virtual writing assistant, do you need help?"
    
    # Call Deepseek API
    response = openai.ChatCompletion.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You're a very good virtual writer. You only speak English."},
            {"role": "user", "content": message}
        ],
        stream=False
    )
    return response.choices[0].message.content

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            message = data.get('message', '').strip()

            if not message:
                self.send_error_response(400, 'No message provided')
                return

            response_text = generate_response(message)
            self.send_success_response(response_text)

        except Exception as e:
            print(f"Error in handler: {e}")
            self.send_error_response(500, str(e))

    def send_success_response(self, response_text):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response_data = json.dumps({'response': response_text})
        self.wfile.write(response_data.encode('utf-8'))

    def send_error_response(self, status_code, error_message):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        error_data = json.dumps({'error': error_message})
        self.wfile.write(error_data.encode('utf-8')) 