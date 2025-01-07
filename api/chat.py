from http.server import BaseHTTPRequestHandler
import json
from openai import OpenAI

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
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No message provided'})
            }

        # Check if it's a greeting question
        if message.lower() in GREETING_QUESTIONS:
            return {
                'statusCode': 200,
                'body': json.dumps({'response': "I'm your virtual writing assistant, do you need help?"})
            }

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
        
        return {
            'statusCode': 200,
            'body': json.dumps({'response': response.choices[0].message.content})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Server Error: {str(e)}'})
        }

def handler(event, context):
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        }
    
    if event['httpMethod'] == 'POST':
        try:
            body = json.loads(event['body'])
            message = body.get('message', '').strip()
            
            response = handle_chat(message)
            response['headers'] = {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
            return response
            
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
    
    return {
        'statusCode': 405,
        'body': json.dumps({'error': 'Method not allowed'}),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    } 