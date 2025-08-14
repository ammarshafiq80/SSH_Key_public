#!/usr/bin/env python3
"""
SSH Key Management API for Gen AI Applications
A RESTful API server for managing SSH keys that can be integrated into generative AI applications.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
import base64
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for Gen AI application integration

# File paths
AUTHORIZED_KEYS_FILE = 'authorized_keys'
SSH_KEY_PUB_FILE = 'ssh_key.pub'

def validate_ssh_key(key_content):
    """Validate SSH key format"""
    try:
        # Remove any trailing newlines or spaces
        key_content = key_content.strip()
        
        # Basic SSH key format validation
        ssh_key_pattern = r'^(ssh-rsa|ssh-ed25519|ssh-dss|ecdsa-sha2-nistp256|ecdsa-sha2-nistp384|ecdsa-sha2-nistp521)\s+[A-Za-z0-9+/=]+(\s+.*)?$'
        
        if not re.match(ssh_key_pattern, key_content):
            return False, "Invalid SSH key format"
        
        parts = key_content.split()
        if len(parts) < 2:
            return False, "SSH key must have at least key type and key data"
        
        key_type = parts[0]
        key_data = parts[1]
        
        # Validate base64 encoding of key data
        try:
            base64.b64decode(key_data)
        except Exception:
            return False, "Invalid base64 encoding in SSH key"
        
        return True, "Valid SSH key"
    
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def read_ssh_keys_from_file(filename):
    """Read SSH keys from a file"""
    keys = []
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                content = f.read().strip()
                if content:
                    # Split by lines and filter out empty lines
                    lines = [line.strip() for line in content.split('\n') if line.strip()]
                    for i, line in enumerate(lines):
                        # Skip numbered lines (like "1." or "2.")
                        if re.match(r'^\d+\.$', line):
                            continue
                        
                        is_valid, message = validate_ssh_key(line)
                        keys.append({
                            'id': i + 1,
                            'key': line,
                            'valid': is_valid,
                            'message': message,
                            'source_file': filename
                        })
    except Exception as e:
        print(f"Error reading {filename}: {str(e)}")
    
    return keys

@app.route('/', methods=['GET'])
def home():
    """API information endpoint"""
    return jsonify({
        'name': 'SSH Key Management API',
        'version': '1.0.0',
        'description': 'REST API for SSH key management in Gen AI applications',
        'endpoints': {
            'GET /': 'This information',
            'GET /keys': 'List all SSH keys',
            'GET /keys/validate': 'Validate SSH key format',
            'POST /keys': 'Add a new SSH key',
            'GET /authorized_keys': 'Get authorized_keys file content',
            'GET /health': 'Health check endpoint'
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'SSH Key Management API'
    })

@app.route('/keys', methods=['GET'])
def get_all_keys():
    """Get all SSH keys from both files"""
    try:
        all_keys = []
        
        # Read from authorized_keys
        auth_keys = read_ssh_keys_from_file(AUTHORIZED_KEYS_FILE)
        all_keys.extend(auth_keys)
        
        # Read from ssh_key.pub
        pub_keys = read_ssh_keys_from_file(SSH_KEY_PUB_FILE)
        all_keys.extend(pub_keys)
        
        return jsonify({
            'success': True,
            'count': len(all_keys),
            'keys': all_keys,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/keys/validate', methods=['POST'])
def validate_key():
    """Validate an SSH key format"""
    try:
        data = request.get_json()
        
        if not data or 'key' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing key in request body'
            }), 400
        
        key_content = data['key']
        is_valid, message = validate_ssh_key(key_content)
        
        return jsonify({
            'success': True,
            'valid': is_valid,
            'message': message,
            'key': key_content,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/keys', methods=['POST'])
def add_key():
    """Add a new SSH key to authorized_keys file"""
    try:
        data = request.get_json()
        
        if not data or 'key' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing key in request body'
            }), 400
        
        key_content = data['key'].strip()
        comment = data.get('comment', f'Added via API at {datetime.now().isoformat()}')
        
        # Validate the key first
        is_valid, validation_message = validate_ssh_key(key_content)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': f'Invalid SSH key: {validation_message}'
            }), 400
        
        # Add comment if not present
        if len(key_content.split()) == 2:
            key_content = f"{key_content} {comment}"
        
        # Append to authorized_keys file
        with open(AUTHORIZED_KEYS_FILE, 'a') as f:
            f.write(f"\n{key_content}\n")
        
        return jsonify({
            'success': True,
            'message': 'SSH key added successfully',
            'key': key_content,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/authorized_keys', methods=['GET'])
def get_authorized_keys():
    """Get the raw content of authorized_keys file"""
    try:
        if not os.path.exists(AUTHORIZED_KEYS_FILE):
            return jsonify({
                'success': False,
                'error': 'authorized_keys file not found'
            }), 404
        
        with open(AUTHORIZED_KEYS_FILE, 'r') as f:
            content = f.read()
        
        return jsonify({
            'success': True,
            'content': content,
            'file': AUTHORIZED_KEYS_FILE,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'timestamp': datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'timestamp': datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    print("Starting SSH Key Management API Server...")
    print("Available endpoints:")
    print("  GET  /                - API information")
    print("  GET  /health          - Health check")
    print("  GET  /keys            - List all SSH keys")
    print("  POST /keys/validate   - Validate SSH key format")
    print("  POST /keys            - Add new SSH key")
    print("  GET  /authorized_keys - Get authorized_keys content")
    print("\nServer running on http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)