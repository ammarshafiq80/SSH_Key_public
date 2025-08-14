# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Clone and Setup
```bash
git clone https://github.com/ammarshafiq80/SSH_Key_public.git
cd SSH_Key_public
./setup.sh
```

### 2. Configure GitHub Token
```bash
# Edit .env file
nano .env

# Add your GitHub token:
GITHUB_TOKEN=your_github_token_here
```

### 3. Start the API
```bash
python app.py
```

### 4. Test the API
```bash
# In another terminal
python examples/test_api.py
```

### 5. Try Interactive Chat
```bash
python examples/chat_example.py
```

## 🔑 Getting GitHub Token

1. Go to [GitHub Settings](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select necessary scopes for GitHub Models
4. Copy and paste the token into your `.env` file

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/chat/completions` | POST | Chat with GPT |
| `/api/completions` | POST | Text completion |
| `/api/models` | GET | List available models |

## 🧪 Example Request

```bash
curl -X POST http://localhost:5000/api/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello, GPT!"}
    ]
  }'
```

## 🐳 Docker Quick Start

```bash
docker build -t github-models-api .
docker run -p 5000:5000 -e GITHUB_TOKEN=your_token github-models-api
```

---

For detailed documentation, see [README.md](README.md).