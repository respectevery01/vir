from openai import OpenAI
import json
from http import HTTPStatus

# Initialize OpenAI client with Deepseek configuration
client = OpenAI(
    api_key="sk-e275a5c8e0684743bf45ab3ebe79607e",
    base_url="https://api.deepseek.com"
)

def generate_response(message):
    try:
        if message.lower() in ["你是谁？", "你是谁", "who are you?", "who are you", "what are you", "what are you?", "who are u"]:
            return "I'm your virtual writing assistant, do you need help?"
        
        print("Sending request to Deepseek API...")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You're a very good virtual writer. You only speak English."},
                {"role": "user", "content": message}
            ],
            stream=False
        )
        print("Response received:", response)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in generate_response: {str(e)}")
        raise e

def handler(request):
    print("Received request:", request)
    
    if request.get('method', '') == 'OPTIONS':
        return {
            'statusCode': HTTPStatus.NO_CONTENT,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Content-Type': 'application/json'
            }
        }

    if request.get('method', '') != 'POST':
        return {
            'statusCode': HTTPStatus.METHOD_NOT_ALLOWED,
            'body': json.dumps({'error': 'Method not allowed'}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            }
        }

    try:
        body = json.loads(request.get('body', '{}'))
        message = body.get('message', '').strip()
        print("Received message:", message)

        if not message:
            return {
                'statusCode': HTTPStatus.BAD_REQUEST,
                'body': json.dumps({'error': 'No message provided'}),
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                }
            }

        response_text = generate_response(message)
        print("Generated response:", response_text)
        
        return {
            'statusCode': HTTPStatus.OK,
            'body': json.dumps({'response': response_text}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            }
        }

    except Exception as e:
        error_message = str(e)
        print(f"Error in handler: {error_message}")
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'error': error_message}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            }
        } 