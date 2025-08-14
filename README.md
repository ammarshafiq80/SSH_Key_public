# GitHub Models GPT API

A REST API wrapper for GitHub Models to access GPT and other AI models through GitHub's AI model marketplace for testing and prototyping.

## Overview

This API provides a simple interface to interact with GitHub Models, making it easy to test and prototype with various AI models including GPT-4, GPT-3.5, and other models available through GitHub's marketplace.

## Features

- 🚀 RESTful API compatible with OpenAI API format
- 🔐 Secure authentication using GitHub tokens
- 📝 Support for chat completions and text completions
- 🔍 Model listing and discovery
- 📊 Comprehensive error handling and logging
- 🐳 Docker support (optional)

## Prerequisites

- Python 3.7 or higher
- GitHub account with access to GitHub Models
- GitHub Personal Access Token

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ammarshafiq80/SSH_Key_public.git
cd SSH_Key_public
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

1. Copy the environment template:
```bash
cp .env.template .env
```

2. Edit `.env` and add your GitHub token:
```bash
GITHUB_TOKEN=your_github_token_here
PORT=5000
DEBUG=False
```

### 4. Get GitHub Token

1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes (you may need specific permissions for GitHub Models)
4. Copy the token and add it to your `.env` file

## Usage

### Starting the API

```bash
python app.py
```

The API will start on `http://localhost:5000` by default.

### API Endpoints

#### Health Check
```http
GET /
```

Response:
```json
{
  "status": "healthy",
  "service": "GitHub Models GPT API",
  "timestamp": "2024-01-01T00:00:00",
  "version": "1.0.0"
}
```

#### Chat Completions
```http
POST /api/chat/completions
```

Request body:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hello, how are you?"
    }
  ],
  "model": "gpt-4o",
  "max_tokens": 1000,
  "temperature": 0.7
}
```

#### Text Completions
```http
POST /api/completions
```

Request body:
```json
{
  "prompt": "The future of AI is",
  "model": "gpt-4o",
  "max_tokens": 100,
  "temperature": 0.7
}
```

#### List Available Models
```http
GET /api/models
```

### Example Usage with curl

#### Chat Completion
```bash
curl -X POST http://localhost:5000/api/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Write a short poem about programming"}
    ],
    "model": "gpt-4o",
    "max_tokens": 200
  }'
```

#### Text Completion
```bash
curl -X POST http://localhost:5000/api/completions \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "The benefits of using GitHub Models include",
    "max_tokens": 150
  }'
```

### Example Usage with Python

```python
import requests

# Chat completion
response = requests.post('http://localhost:5000/api/chat/completions', json={
    'messages': [
        {'role': 'user', 'content': 'Explain quantum computing in simple terms'}
    ],
    'model': 'gpt-4o',
    'max_tokens': 300
})

print(response.json())
```

## API Parameters

### Chat Completions Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `messages` | array | required | Array of message objects |
| `model` | string | "gpt-4o" | Model to use for completion |
| `max_tokens` | integer | 1000 | Maximum tokens to generate |
| `temperature` | float | 0.7 | Sampling temperature (0-2) |
| `top_p` | float | 1.0 | Nucleus sampling parameter |
| `stream` | boolean | false | Whether to stream responses |

### Text Completions Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | required | Text prompt for completion |
| `model` | string | "gpt-4o" | Model to use for completion |
| `max_tokens` | integer | 1000 | Maximum tokens to generate |
| `temperature` | float | 0.7 | Sampling temperature (0-2) |
| `top_p` | float | 1.0 | Nucleus sampling parameter |

## Available Models

The API supports various models available through GitHub Models marketplace:

- `gpt-4o` - GPT-4 Omni model
- `gpt-4` - GPT-4 model
- `gpt-3.5-turbo` - GPT-3.5 Turbo model
- And other models available in GitHub Models

To see all available models, use the `/api/models` endpoint.

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400` - Bad Request (missing or invalid parameters)
- `401` - Unauthorized (invalid or missing GitHub token)
- `500` - Internal Server Error
- `502` - Bad Gateway (GitHub Models API error)

Example error response:
```json
{
  "error": "GitHub Models API request failed",
  "message": "Detailed error message"
}
```

## Development

### Running in Development Mode

```bash
export DEBUG=True
python app.py
```

### Testing

You can test the API using the provided example scripts or any HTTP client like Postman, curl, or Python requests.

## Docker Support

### Build Docker Image

```bash
docker build -t github-models-api .
```

### Run Docker Container

```bash
docker run -p 5000:5000 -e GITHUB_TOKEN=your_token github-models-api
```

## Deployment

### Using Gunicorn

```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

### Environment Variables for Production

```bash
export GITHUB_TOKEN=your_github_token
export PORT=5000
export DEBUG=False
export LOG_LEVEL=INFO
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Resources

- [GitHub Models Documentation](https://docs.github.com/en/github-models/use-github-models/prototyping-with-ai-models)
- [GitHub Models Marketplace](https://github.com/marketplace?type=models)
- [GitHub Personal Access Tokens](https://github.com/settings/tokens)

## Support

If you encounter any issues or have questions, please open an issue in the GitHub repository.

---

**Note**: This API is designed for testing and prototyping purposes. For production use, consider implementing additional security measures, rate limiting, and monitoring.