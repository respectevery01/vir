from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client with Deepseek configuration
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY", "sk-e275a5c8e0684743bf45ab3ebe79607e"),
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

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '').strip().lower()
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400

        # Check if it's a greeting question
        if message in GREETING_QUESTIONS:
            return jsonify({'response': "I'm your virtual writing assistant, do you need help?"})

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
        
        return jsonify({'response': response.choices[0].message.content})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Server Error: {str(e)}'}), 500

# Vercel requires a handler function
def handler(request):
    with app.request_context(request):
        return app.handle_request() 