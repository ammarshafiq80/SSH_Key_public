#!/usr/bin/env python3
"""
Simple interactive chat example using GitHub Models GPT API
"""

import requests
import json
import os
import sys

# Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')

def chat_with_gpt():
    """Interactive chat session with GPT"""
    print("🤖 GitHub Models GPT Chat")
    print("Type 'quit' or 'exit' to end the conversation")
    print("-" * 50)
    
    messages = []
    
    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Add user message to conversation
            messages.append({"role": "user", "content": user_input})
            
            # Prepare API request
            data = {
                "messages": messages,
                "model": "gpt-4o",
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            print("🤔 Thinking...")
            
            # Make API request
            response = requests.post(f"{API_BASE_URL}/api/chat/completions", json=data)
            response.raise_for_status()
            result = response.json()
            
            # Extract assistant response
            if 'choices' in result and len(result['choices']) > 0:
                assistant_message = result['choices'][0]['message']['content']
                messages.append({"role": "assistant", "content": assistant_message})
                
                print(f"🤖 GPT: {assistant_message}")
            else:
                print("❌ No response received from GPT")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
            print("Make sure the API is running and your GitHub token is configured correctly.")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

def main():
    """Main function"""
    # Test API connection first
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        response.raise_for_status()
        print("✅ Connected to GitHub Models GPT API")
    except Exception as e:
        print(f"❌ Failed to connect to API: {e}")
        print("Make sure the API is running with: python app.py")
        sys.exit(1)
    
    # Start chat
    chat_with_gpt()

if __name__ == "__main__":
    main()