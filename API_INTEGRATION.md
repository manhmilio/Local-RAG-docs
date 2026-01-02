# API Integration Guide - Hướng Dẫn Tích Hợp API

## Tổng Quan

Medical Chatbot API cho phép bạn tích hợp chatbot chẩn đoán bệnh với RAG vào bất kỳ dự án web nào thông qua REST API.

**Base URL**: `http://localhost:8001` (hoặc URL server của bạn)

**API Documentation**: `/docs` (Swagger UI) hoặc `/redoc` (ReDoc)

---

## Cấu Hình Backend

### 1. Bật/Tắt Xác Thực API Key

Tạo file `.env` trong thư mục `backend/`:

```env
# CORS Configuration
ALLOW_ALL_ORIGINS=true  # Cho phép tất cả origins
CORS_ORIGINS=http://localhost:3000,http://example.com  # Hoặc chỉ định cụ thể

# API Key Authentication
ENABLE_API_KEY_AUTH=true  # true = bật xác thực, false = tắt
API_KEYS=your-secret-key-1,your-secret-key-2,another-key-here

# Rate Limiting
ENABLE_RATE_LIMITING=true
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

### 2. Tạo API Key Mới

```python
# Chạy script này để tạo API key mới
import secrets
api_key = secrets.token_urlsafe(32)
print(f"New API Key: {api_key}")
```

Sau đó thêm key vào `.env`:
```env
API_KEYS=existing-key,NEW_KEY_HERE
```

---

## Endpoints Chính

### 1. **GET /** - Thông Tin API

Lấy thông tin tổng quan về API.

**Request:**
```bash
curl http://localhost:8001/
```

**Response:**
```json
{
  "message": "Medical Chatbot API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health",
  "endpoints": {
    "chat": "/chat",
    "chat_stream": "/chat/stream",
    "upload": "/documents/upload",
    "stats": "/documents/stats"
  },
  "authentication": false,
  "rate_limiting": true
}
```

---

### 2. **GET /api/info** - Chi Tiết Cấu Hình

Lấy thông tin chi tiết về model, features, và limits.

**Request:**
```bash
curl http://localhost:8001/api/info
```

**Response:**
```json
{
  "api_version": "1.0.0",
  "model": "mistral:7b",
  "embedding_model": "paraphrase-multilingual-MiniLM-L12-v2",
  "features": {
    "rag_enabled": true,
    "streaming_support": true,
    "document_upload": true,
    "multilingual": true
  },
  "limits": {
    "max_tokens": 2048,
    "rate_limit_per_minute": 60,
    "rate_limit_per_hour": 1000
  },
  "authentication": {
    "required": false,
    "method": "None"
  },
  "cors": {
    "allow_all_origins": true,
    "allowed_origins": ["*"]
  }
}
```

---

### 3. **POST /chat** - Chat Cơ Bản

Gửi câu hỏi và nhận câu trả lời.

**Request:**
```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key-here" \
  -d '{
    "message": "Triệu chứng sốt và ho có thể là bệnh gì?",
    "conversation_history": [],
    "use_rag": true
  }'
```

**With JavaScript:**
```javascript
async function chat(message) {
  const response = await fetch('http://localhost:8001/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': 'your-api-key-here'  // Nếu bật authentication
    },
    body: JSON.stringify({
      message: message,
      conversation_history: [],
      use_rag: true
    })
  });
  
  const data = await response.json();
  return data;
}

// Sử dụng
const result = await chat("Triệu chứng sốt và ho?");
console.log(result.response);
```

**Response:**
```json
{
  "response": "Dựa trên triệu chứng sốt và ho, có thể là...",
  "sources": [
    {
      "content": "Văn bản tham khảo từ tài liệu...",
      "metadata": {
        "source": "medical_guide.pdf",
        "page": 15
      },
      "similarity": 0.85
    }
  ]
}
```

---

### 4. **POST /chat/stream** - Chat Streaming

Nhận response theo thời gian thực (SSE - Server-Sent Events).

**With JavaScript:**
```javascript
async function chatStream(message) {
  const response = await fetch('http://localhost:8001/chat/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': 'your-api-key-here'
    },
    body: JSON.stringify({
      message: message,
      conversation_history: [],
      use_rag: true
    })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    const chunk = decoder.decode(value);
    const lines = chunk.split('\n');
    
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));
        console.log(data.chunk);  // In từng chunk
      }
    }
  }
}

chatStream("Triệu chứng đau đầu?");
```

---

### 5. **POST /documents/upload** - Upload Tài Liệu

Upload PDF để thêm vào knowledge base.

**Note**: Endpoint này **yêu cầu API key** nếu authentication được bật.

**Request:**
```bash
curl -X POST http://localhost:8001/documents/upload \
  -H "X-API-Key: your-api-key-here" \
  -F "file=@medical_document.pdf"
```

**With JavaScript:**
```javascript
async function uploadDocument(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('http://localhost:8001/documents/upload', {
    method: 'POST',
    headers: {
      'X-API-Key': 'your-api-key-here'
    },
    body: formData
  });

  return await response.json();
}

// Sử dụng với file input
const fileInput = document.querySelector('input[type="file"]');
fileInput.addEventListener('change', async (e) => {
  const file = e.target.files[0];
  const result = await uploadDocument(file);
  console.log(result);
});
```

**Response:**
```json
{
  "filename": "medical_document.pdf",
  "chunks_created": 45,
  "status": "success",
  "message": "Đã xử lý thành công 45 chunks từ medical_document.pdf"
}
```

---

### 6. **GET /documents/stats** - Thống Kê Tài Liệu

Lấy thông tin về số lượng documents trong vector store.

**Request:**
```bash
curl http://localhost:8001/documents/stats
```

**Response:**
```json
{
  "total_documents": 150,
  "total_chunks": 1250,
  "collection_name": "medical_documents"
}
```

---

### 7. **GET /health** - Health Check

Kiểm tra trạng thái hệ thống.

**Request:**
```bash
curl http://localhost:8001/health
```

**Response:**
```json
{
  "status": "healthy",
  "ollama_connected": true,
  "chroma_initialized": true
}
```

---

## Ví Dụ Tích Hợp

### React Application

```jsx
import React, { useState } from 'react';

function ChatComponent() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const API_URL = 'http://localhost:8001';
  const API_KEY = 'your-api-key-here';  // Nếu cần

  const sendMessage = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': API_KEY
        },
        body: JSON.stringify({
          message: message,
          conversation_history: [],
          use_rag: true
        })
      });

      const data = await res.json();
      setResponse(data.response);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input 
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Nhập câu hỏi..."
      />
      <button onClick={sendMessage} disabled={loading}>
        {loading ? 'Đang xử lý...' : 'Gửi'}
      </button>
      {response && <div>{response}</div>}
    </div>
  );
}
```

---

### Vue.js Application

```vue
<template>
  <div>
    <input v-model="message" placeholder="Nhập câu hỏi..." />
    <button @click="sendMessage" :disabled="loading">
      {{ loading ? 'Đang xử lý...' : 'Gửi' }}
    </button>
    <div v-if="response">{{ response }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: '',
      response: '',
      loading: false,
      apiUrl: 'http://localhost:8001',
      apiKey: 'your-api-key-here'
    }
  },
  methods: {
    async sendMessage() {
      this.loading = true;
      try {
        const res = await fetch(`${this.apiUrl}/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-API-Key': this.apiKey
          },
          body: JSON.stringify({
            message: this.message,
            conversation_history: [],
            use_rag: true
          })
        });

        const data = await res.json();
        this.response = data.response;
      } catch (error) {
        console.error('Error:', error);
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>
```

---

### Plain HTML + JavaScript

```html
<!DOCTYPE html>
<html>
<head>
  <title>Medical Chatbot</title>
</head>
<body>
  <input id="messageInput" placeholder="Nhập câu hỏi..." />
  <button onclick="sendMessage()">Gửi</button>
  <div id="response"></div>

  <script>
    const API_URL = 'http://localhost:8001';
    const API_KEY = 'your-api-key-here';

    async function sendMessage() {
      const message = document.getElementById('messageInput').value;
      
      try {
        const response = await fetch(`${API_URL}/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-API-Key': API_KEY
          },
          body: JSON.stringify({
            message: message,
            conversation_history: [],
            use_rag: true
          })
        });

        const data = await response.json();
        document.getElementById('response').innerText = data.response;
      } catch (error) {
        console.error('Error:', error);
      }
    }
  </script>
</body>
</html>
```

---

## Xử Lý Lỗi

### HTTP Status Codes

- **200**: Success
- **400**: Bad Request (invalid input)
- **401**: Unauthorized (invalid/missing API key)
- **429**: Too Many Requests (rate limit exceeded)
- **500**: Internal Server Error

### Error Response Format

```json
{
  "detail": "Error message here"
}
```

### Rate Limiting Headers

Khi gặp rate limit, response sẽ có các headers:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1735852800
Retry-After: 60
```

**Example Error Handling:**
```javascript
async function chatWithErrorHandling(message) {
  try {
    const response = await fetch('http://localhost:8001/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': 'your-api-key'
      },
      body: JSON.stringify({
        message: message,
        conversation_history: [],
        use_rag: true
      })
    });

    if (response.status === 429) {
      const retryAfter = response.headers.get('Retry-After');
      throw new Error(`Rate limit exceeded. Retry after ${retryAfter} seconds`);
    }

    if (response.status === 401) {
      throw new Error('Invalid API key');
    }

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }

    return await response.json();
  } catch (error) {
    console.error('Chat error:', error);
    throw error;
  }
}
```

---

## Best Practices

### 1. **Quản Lý API Key**

```javascript
// Đừng hardcode API key trong code
// Sử dụng environment variables
const API_KEY = process.env.REACT_APP_API_KEY;

// Hoặc config file
import config from './config';
const API_KEY = config.apiKey;
```

### 2. **Retry Logic cho Rate Limiting**

```javascript
async function chatWithRetry(message, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await chat(message);
    } catch (error) {
      if (error.status === 429 && i < maxRetries - 1) {
        const retryAfter = parseInt(error.headers.get('Retry-After') || '60');
        await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
        continue;
      }
      throw error;
    }
  }
}
```

### 3. **Caching Responses**

```javascript
const responseCache = new Map();

async function chatWithCache(message) {
  if (responseCache.has(message)) {
    return responseCache.get(message);
  }

  const response = await chat(message);
  responseCache.set(message, response);
  return response;
}
```

### 4. **Timeout Handling**

```javascript
async function chatWithTimeout(message, timeout = 30000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch('http://localhost:8001/chat', {
      method: 'POST',
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': 'your-api-key'
      },
      body: JSON.stringify({
        message: message,
        conversation_history: [],
        use_rag: true
      })
    });

    return await response.json();
  } finally {
    clearTimeout(timeoutId);
  }
}
```

---

## Testing

### Test với cURL

```bash
# Test without authentication
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "conversation_history": [], "use_rag": true}'

# Test with API key
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"message": "Hello", "conversation_history": [], "use_rag": true}'

# Test health
curl http://localhost:8001/health

# Test info
curl http://localhost:8001/api/info
```

### Test với Postman

1. Import các endpoints từ `/openapi.json`
2. Tạo environment với biến `API_KEY`
3. Thêm header `X-API-Key` vào collection

---

## Troubleshooting

### CORS Errors

Nếu gặp lỗi CORS:

1. Bật `ALLOW_ALL_ORIGINS=true` trong `.env`
2. Hoặc thêm origin của bạn vào `CORS_ORIGINS`

```env
CORS_ORIGINS=http://localhost:3000,https://myapp.com
```

### Authentication Errors

```bash
# Kiểm tra API key có đúng không
curl http://localhost:8001/api/info

# Nếu authentication bật, response sẽ có "required": true
```

### Rate Limiting

```bash
# Tăng limits trong .env
RATE_LIMIT_PER_MINUTE=120
RATE_LIMIT_PER_HOUR=2000

# Hoặc tắt hoàn toàn
ENABLE_RATE_LIMITING=false
```

---

## Contact & Support

- **Documentation**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/health
- **API Info**: http://localhost:8001/api/info
