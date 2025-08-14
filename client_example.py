#!/usr/bin/env python3
"""
SSH Key API Client
Example client for demonstrating how to use the SSH Key Management API in Gen AI applications.
"""

import requests
import json
import sys

class SSHKeyAPIClient:
    def __init__(self, api_url="http://localhost:5000"):
        self.api_url = api_url.rstrip('/')
    
    def get_api_info(self):
        """Get API information"""
        response = requests.get(f"{self.api_url}/")
        return response.json()
    
    def health_check(self):
        """Check API health"""
        response = requests.get(f"{self.api_url}/health")
        return response.json()
    
    def get_all_keys(self):
        """Get all SSH keys"""
        response = requests.get(f"{self.api_url}/keys")
        return response.json()
    
    def validate_key(self, ssh_key):
        """Validate an SSH key"""
        response = requests.post(f"{self.api_url}/keys/validate", json={"key": ssh_key})
        return response.json()
    
    def add_key(self, ssh_key, comment=None):
        """Add a new SSH key"""
        data = {"key": ssh_key}
        if comment:
            data["comment"] = comment
        response = requests.post(f"{self.api_url}/keys", json=data)
        return response.json()
    
    def get_authorized_keys(self):
        """Get authorized_keys file content"""
        response = requests.get(f"{self.api_url}/authorized_keys")
        return response.json()

def main():
    print("🔑 SSH Key Management API Client")
    print("=" * 40)
    
    # Initialize client
    client = SSHKeyAPIClient()
    
    try:
        # Test API connection
        print("1. Testing API connection...")
        health = client.health_check()
        print(f"   ✅ API Status: {health['status']}")
        
        # Get API info
        print("\n2. Getting API information...")
        api_info = client.get_api_info()
        print(f"   📋 API Name: {api_info['name']}")
        print(f"   📋 Version: {api_info['version']}")
        
        # Get all existing keys
        print("\n3. Fetching existing SSH keys...")
        keys_response = client.get_all_keys()
        print(f"   🔑 Found {keys_response['count']} SSH keys")
        
        for i, key in enumerate(keys_response['keys'], 1):
            print(f"   Key {i}: {key['source_file']} - {'✅ Valid' if key['valid'] else '❌ Invalid'}")
            print(f"           {key['key'][:50]}...")
        
        # Example: Validate a test key
        print("\n4. Testing key validation...")
        test_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDQmcvK1sDCKXak test@genai.app"
        validation_result = client.validate_key(test_key)
        print(f"   🔍 Test Key Valid: {'✅ Yes' if validation_result['valid'] else '❌ No'}")
        print(f"   🔍 Message: {validation_result['message']}")
        
        # Example integration patterns for Gen AI applications
        print("\n5. 🤖 Gen AI Integration Examples:")
        print("   📝 Use case 1: Validate user-provided SSH keys before deployment")
        print("   📝 Use case 2: Manage SSH keys for automated server provisioning")
        print("   📝 Use case 3: Store and retrieve SSH keys for CI/CD pipelines")
        print("   📝 Use case 4: Validate keys in infrastructure-as-code generation")
        
        print("\n✨ API is ready for your Gen AI application!")
        print(f"   Base URL: {client.api_url}")
        print("   See README.md for detailed integration examples")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API server")
        print("   Make sure the API server is running: python api_server.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()