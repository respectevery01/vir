from http.server import BaseHTTPRequestHandler
import openai
import json

openai.api_key = "sk-e275a5c8e0684743bf45ab3ebe79607e"
openai.api_base = "https://api.deepseek.com/v1"

def generate_response(message):
    # Convert message to lowercase for case-insensitive comparison
    msg_lower = message.lower()
    
    # Identity questions
    if msg_lower in ["你是谁？", "你是谁", "who are you?", "who are you", "what are you", "what are you?", "who are u"]:
        return "I'm your virtual writing assistant, do you need help?"
    
    # Capability questions
    if msg_lower in ["what can you do", "what can you do?", "help", "help me", "你能做什么", "你能做什么？"]:
        return "Sir, I can help you finish your novel. Please tell me the genre of your novel."
    
    # Questions about words and phrases
    if any(q in msg_lower for q in ["what is word", "what's word", "what are words", "what is phrase", "what's phrase", 
                                   "什么是短语", "什么是词", "词是什么", "短语是什么"]):
        return "Words are the ephemeral bridges we build over the abyss of silence. Each phrase, fragile and fleeting, is an act of rebellion against the inevitable erasure that time brings. Yet, in their impermanence lies their beauty—like fireflies in the dark."
    
    # Questions about writing motivation
    if any(q in msg_lower for q in ["why do you write", "why write", "why do we write", "why writing", 
                                   "你为什么写作", "为什么写作", "我们为什么写作"]):
        return "The void whispers in every silence, a reminder that creation is rebellion. We write, not to hold onto meaning, but to defy the nothingness. Perhaps the fleeting nature of our words is the only proof they ever existed at all."
    
    # Call Deepseek API for other messages
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