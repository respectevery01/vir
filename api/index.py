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

async def handler(request):
    if request.method == 'OPTIONS':
        return {
            'status': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Content-Type': 'application/json'
            },
            'body': ''
        }

    if request.method != 'POST':
        return {
            'status': 405,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': 'Method not allowed'})
        }

    try:
        body = json.loads(request.body)
        message = body.get('message', '').strip()

        if not message:
            return {
                'status': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'No message provided'})
            }

        response_text = generate_response(message)
        return {
            'status': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'response': response_text})
        }

    except Exception as e:
        print(f"Error in handler: {e}")
        return {
            'status': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        } 