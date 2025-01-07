from openai import OpenAI
import json

# Initialize OpenAI client
client = OpenAI(
    api_key="sk-e275a5c8e0684743bf45ab3ebe79607e",
    base_url="https://api.deepseek.com/v1"
)

def generate_response(message):
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

def handler(request):
    """
    request - dict with the following keys:
    - httpMethod: HTTP method
    - body: Request body (if any)
    - headers: Request headers
    """
    # Handle CORS preflight request
    if request.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 204,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Content-Type': 'application/json'
            }
        }

    # Only allow POST method
    if request.get('httpMethod') != 'POST':
        return {
            'statusCode': 405,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': 'Method not allowed'})
        }

    try:
        # Parse request body
        body = json.loads(request.get('body', '{}'))
        message = body.get('message', '').strip()

        if not message:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'No message provided'})
            }

        # Generate response
        response_text = generate_response(message)
        
        # Return success response
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'response': response_text})
        }

    except Exception as e:
        print(f"Error in handler: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        } 