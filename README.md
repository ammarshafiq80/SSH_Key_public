# SSH Key Management API

A RESTful API server for managing SSH keys that can be easily integrated into generative AI applications.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API server:**
   ```bash
   python api_server.py
   ```

3. **Access the API:**
   The server runs on `http://localhost:5000`

## API Endpoints

### 1. Get API Information
```http
GET /
```
Returns information about the API and available endpoints.

### 2. Health Check
```http
GET /health
```
Health check endpoint for monitoring.

### 3. List All SSH Keys
```http
GET /keys
```
Returns all SSH keys from both `authorized_keys` and `ssh_key.pub` files.

**Response:**
```json
{
  "success": true,
  "count": 2,
  "keys": [
    {
      "id": 1,
      "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDQmcvK1sDCKXak...",
      "valid": true,
      "message": "Valid SSH key",
      "source_file": "authorized_keys"
    }
  ],
  "timestamp": "2023-12-07T10:30:00"
}
```

### 4. Validate SSH Key
```http
POST /keys/validate
Content-Type: application/json

{
  "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDQmcvK1sDCKXak... user@host"
}
```

**Response:**
```json
{
  "success": true,
  "valid": true,
  "message": "Valid SSH key",
  "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDQmcvK1sDCKXak... user@host",
  "timestamp": "2023-12-07T10:30:00"
}
```

### 5. Add New SSH Key
```http
POST /keys
Content-Type: application/json

{
  "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDQmcvK1sDCKXak... user@host",
  "comment": "Added for Gen AI application"
}
```

**Response:**
```json
{
  "success": true,
  "message": "SSH key added successfully",
  "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDQmcvK1sDCKXak... user@host",
  "timestamp": "2023-12-07T10:30:00"
}
```

### 6. Get Authorized Keys File
```http
GET /authorized_keys
```
Returns the raw content of the `authorized_keys` file.

## Integration with Gen AI Applications

### Python Example
```python
import requests

# API base URL
API_URL = "http://localhost:5000"

# Get all SSH keys
response = requests.get(f"{API_URL}/keys")
keys_data = response.json()

# Validate a new SSH key
new_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDQmcvK1sDCKXak... user@host"
validation_response = requests.post(f"{API_URL}/keys/validate", json={"key": new_key})
is_valid = validation_response.json()["valid"]

# Add a new SSH key if valid
if is_valid:
    add_response = requests.post(f"{API_URL}/keys", json={
        "key": new_key,
        "comment": "Added by Gen AI application"
    })
    print("Key added:", add_response.json())
```

### JavaScript/Node.js Example
```javascript
const axios = require('axios');

const API_URL = 'http://localhost:5000';

// Get all SSH keys
async function getAllKeys() {
    try {
        const response = await axios.get(`${API_URL}/keys`);
        return response.data.keys;
    } catch (error) {
        console.error('Error fetching keys:', error);
    }
}

// Validate and add SSH key
async function addSSHKey(sshKey, comment = 'Added via Gen AI app') {
    try {
        // First validate
        const validateResponse = await axios.post(`${API_URL}/keys/validate`, { key: sshKey });
        
        if (validateResponse.data.valid) {
            // Add the key
            const addResponse = await axios.post(`${API_URL}/keys`, { 
                key: sshKey, 
                comment: comment 
            });
            return addResponse.data;
        } else {
            throw new Error(`Invalid SSH key: ${validateResponse.data.message}`);
        }
    } catch (error) {
        console.error('Error adding SSH key:', error);
        throw error;
    }
}
```

### cURL Examples
```bash
# Get all keys
curl -X GET http://localhost:5000/keys

# Validate a key
curl -X POST http://localhost:5000/keys/validate \
  -H "Content-Type: application/json" \
  -d '{"key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDQmcvK1sDCKXak... user@host"}'

# Add a new key
curl -X POST http://localhost:5000/keys \
  -H "Content-Type: application/json" \
  -d '{"key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDQmcvK1sDCKXak... user@host", "comment": "Gen AI key"}'
```

## Features

- ✅ **RESTful API** - Clean HTTP endpoints for all operations
- ✅ **SSH Key Validation** - Validates key format and base64 encoding
- ✅ **CORS Support** - Ready for web application integration
- ✅ **Error Handling** - Comprehensive error responses
- ✅ **JSON Responses** - All responses in JSON format
- ✅ **Health Monitoring** - Health check endpoint for monitoring
- ✅ **Multiple Key Sources** - Reads from both authorized_keys and ssh_key.pub
- ✅ **Key Management** - Add new keys with automatic validation

## Error Responses

All errors follow a consistent format:
```json
{
  "success": false,
  "error": "Description of the error",
  "timestamp": "2023-12-07T10:30:00"
}
```

## Security Considerations

- The API validates all SSH keys before adding them
- CORS is enabled for web application integration
- Consider adding authentication for production use
- Run behind a reverse proxy (nginx) for production deployment

## Production Deployment

For production use, consider:
1. Adding authentication (API keys, JWT, etc.)
2. Using a production WSGI server (gunicorn, uwsgi)
3. Setting up SSL/TLS certificates
4. Implementing rate limiting
5. Adding logging and monitoring