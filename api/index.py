from flask import Flask, request, jsonify
from openai import OpenAI
import json

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(
    api_key="sk-e275a5c8e0684743bf45ab3ebe79607e",
    base_url="https://api.deepseek.com/v1"
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

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def handler():
    # Handle CORS preflight request
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response

    try:
        data = request.get_json()
        message = data.get('message', '').strip()

        if not message:
            return jsonify({'error': 'No message provided'}), 400

        response_text = generate_response(message)
        response = jsonify({'response': response_text})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except Exception as e:
        print(f"Error in handler: {e}")
        error_response = jsonify({'error': str(e)})
        error_response.headers.add('Access-Control-Allow-Origin', '*')
        return error_response, 500 