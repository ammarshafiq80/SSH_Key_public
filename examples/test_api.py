#!/usr/bin/env python3
"""
Example script demonstrating how to use the GitHub Models GPT API
"""

import requests
import json
import sys
import os

# Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        response.raise_for_status()
        print(f"✅ Health check passed: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_chat_completion():
    """Test chat completion endpoint"""
    print("\nTesting chat completion...")
    try:
        data = {
            "messages": [
                {"role": "user", "content": "Write a haiku about programming"}
            ],
            "model": "gpt-4o",
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        response = requests.post(f"{API_BASE_URL}/api/chat/completions", json=data)
        response.raise_for_status()
        result = response.json()
        
        print("✅ Chat completion successful!")
        if 'choices' in result and len(result['choices']) > 0:
            print(f"Response: {result['choices'][0]['message']['content']}")
        else:
            print(f"Full response: {json.dumps(result, indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Chat completion failed: {e}")
        return False

def test_text_completion():
    """Test text completion endpoint"""
    print("\nTesting text completion...")
    try:
        data = {
            "prompt": "The future of artificial intelligence is",
            "model": "gpt-4o",
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        response = requests.post(f"{API_BASE_URL}/api/completions", json=data)
        response.raise_for_status()
        result = response.json()
        
        print("✅ Text completion successful!")
        if 'choices' in result and len(result['choices']) > 0:
            print(f"Response: {result['choices'][0]['text']}")
        else:
            print(f"Full response: {json.dumps(result, indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Text completion failed: {e}")
        return False

def test_list_models():
    """Test list models endpoint"""
    print("\nTesting list models...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/models")
        response.raise_for_status()
        result = response.json()
        
        print("✅ List models successful!")
        if 'data' in result:
            print(f"Available models: {len(result['data'])}")
            for model in result['data'][:5]:  # Show first 5 models
                print(f"  - {model.get('id', 'Unknown')}")
        else:
            print(f"Response: {json.dumps(result, indent=2)}")
        return True
    except Exception as e:
        print(f"❌ List models failed: {e}")
        return False

def main():
    """Run all tests"""
    print("GitHub Models GPT API - Example Usage")
    print("=" * 40)
    
    # Check if API is running
    if not test_health_check():
        print("\n❌ API is not running or not accessible!")
        print("Make sure to start the API with: python app.py")
        sys.exit(1)
    
    # Run tests
    tests = [
        test_chat_completion,
        test_text_completion,
        test_list_models
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n{'='*40}")
    print(f"Tests completed: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check your GitHub token and API configuration.")
        sys.exit(1)

if __name__ == "__main__":
    main()