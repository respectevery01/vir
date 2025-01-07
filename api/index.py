from openai import OpenAI
import json
from http.server import BaseHTTPRequestHandler
from http import HTTPStatus

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

def handler(request):
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
        return {
            'statusCode': HTTPStatus.OK,
            'body': json.dumps({'response': response_text}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            }
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            }
        } 