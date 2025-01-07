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

def handler(event, context):
    """
    Vercel serverless function handler
    """
    # Set default headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }

    # Handle CORS preflight request
    if event.get('httpMethod', '').upper() == 'OPTIONS':
        return {
            'statusCode': 204,
            'headers': headers,
            'body': ''
        }

    # Only allow POST method
    if event.get('httpMethod', '').upper() != 'POST':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({'error': 'Method not allowed'})
        }

    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        message = body.get('message', '').strip()

        if not message:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'No message provided'})
            }

        # Generate response
        response_text = generate_response(message)
        
        # Return success response
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'response': response_text})
        }

    except Exception as e:
        print(f"Error in handler: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        } 