"""
GitHub Models GPT API
A REST API wrapper for GitHub Models to access GPT through GitHub's AI model marketplace
"""

import logging
from flask import Flask, request, jsonify
import requests
from datetime import datetime, timezone
from functools import wraps
from config import config

# Configure logging
logging.basicConfig(level=getattr(logging, config.log_level))
logger = logging.getLogger(__name__)

app = Flask(__name__)

def require_auth(f):
    """Decorator to require GitHub token authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not config.is_valid():
            return jsonify({
                'error': 'GitHub token not configured',
                'message': 'Please set GITHUB_TOKEN environment variable'
            }), 500
        return f(*args, **kwargs)
    return decorated_function

def make_github_models_request(endpoint, data, model=None):
    """Make a request to GitHub Models API"""
    headers = config.get_github_headers()
    
    # Use configured base URL
    url = f"{config.github_models_base_url}/{endpoint}"
    
    # Apply default model if not specified
    if model is None and 'model' not in data:
        data['model'] = config.default_model
    
    try:
        logger.info(f"Making request to GitHub Models: {endpoint}")
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"GitHub Models API request failed: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                logger.error(f"Error details: {error_detail}")
            except:
                logger.error(f"Response text: {e.response.text}")
        raise

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'GitHub Models GPT API',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/chat/completions', methods=['POST'])
@require_auth
def chat_completions():
    """
    Create chat completions using GitHub Models GPT
    Compatible with OpenAI chat completions API format
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        if 'messages' not in data:
            return jsonify({'error': 'messages field is required'}), 400
        
        # Default model if not specified
        model = data.get('model', config.default_model)
        
        # Prepare request for GitHub Models
        github_request = {
            'messages': data['messages'],
            'model': model,
            'max_tokens': data.get('max_tokens', config.default_max_tokens),
            'temperature': data.get('temperature', config.default_temperature),
            'top_p': data.get('top_p', 1.0),
            'stream': data.get('stream', False)
        }
        
        # Make request to GitHub Models
        response = make_github_models_request('chat/completions', github_request)
        
        return jsonify(response)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"GitHub Models request failed: {str(e)}")
        return jsonify({
            'error': 'GitHub Models API request failed',
            'message': str(e)
        }), 502
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/models', methods=['GET'])
@require_auth
def list_models():
    """List available models from GitHub Models"""
    try:
        headers = config.get_github_headers()
        
        response = requests.get(f"{config.github_models_base_url}/models", headers=headers, timeout=30)
        response.raise_for_status()
        
        return jsonify(response.json())
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch models: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch models',
            'message': str(e)
        }), 502
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/completions', methods=['POST'])
@require_auth
def completions():
    """
    Create text completions using GitHub Models GPT
    Compatible with OpenAI completions API format
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        if 'prompt' not in data:
            return jsonify({'error': 'prompt field is required'}), 400
        
        # Convert to chat format for GitHub Models
        messages = [{'role': 'user', 'content': data['prompt']}]
        
        github_request = {
            'messages': messages,
            'model': data.get('model', config.default_model),
            'max_tokens': data.get('max_tokens', config.default_max_tokens),
            'temperature': data.get('temperature', config.default_temperature),
            'top_p': data.get('top_p', 1.0)
        }
        
        response = make_github_models_request('chat/completions', github_request)
        
        # Convert back to completions format
        if 'choices' in response and len(response['choices']) > 0:
            response['choices'][0]['text'] = response['choices'][0]['message']['content']
            del response['choices'][0]['message']
        
        return jsonify(response)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"GitHub Models request failed: {str(e)}")
        return jsonify({
            'error': 'GitHub Models API request failed',
            'message': str(e)
        }), 502
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Check if GitHub token is set
    if not config.is_valid():
        print("WARNING: GITHUB_TOKEN environment variable not set!")
        print("The API will not work without a valid GitHub token.")
    
    # Run the app
    print(f"Starting GitHub Models GPT API on port {config.port}")
    app.run(host='0.0.0.0', port=config.port, debug=config.debug)