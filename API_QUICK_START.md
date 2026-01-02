# Cấu Hình API cho Dự Án Khác

## Tóm Tắt Những Gì Đã Cập Nhật

✅ **CORS Configuration** - Cho phép kết nối từ bất kỳ domain nào  
✅ **API Key Authentication** - Bảo mật API với khóa xác thực  
✅ **Rate Limiting** - Giới hạn số request để tránh abuse  
✅ **API Documentation** - Tài liệu chi tiết về tích hợp  
✅ **New Endpoints** - `/api/info` để lấy thông tin hệ thống  

---

## Quick Start - Sử Dụng API

### 1. Cấu Hình Backend (Không Cần Authentication)

Tạo file `.env` trong `backend/`:

```env
ALLOW_ALL_ORIGINS=true
ENABLE_API_KEY_AUTH=false
ENABLE_RATE_LIMITING=true
```

### 2. Khởi Động Backend

```bash
cd backend
python main.py
```

### 3. Test API

```bash
# Kiểm tra API info
curl http://localhost:8001/api/info

# Test chat
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "conversation_history": [], "use_rag": true}'
```

---

## Tích Hợp Vào Dự Án Khác

### React / Next.js

```javascript
const API_URL = 'http://localhost:8001';

async function chat(message) {
  const response = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message: message,
      conversation_history: [],
      use_rag: true
    })
  });
  
  return await response.json();
}
```

### Vue.js

```javascript
async sendMessage() {
  const res = await fetch('http://localhost:8001/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: this.message,
      conversation_history: [],
      use_rag: true
    })
  });
  
  const data = await res.json();
  this.response = data.response;
}
```

### Plain JavaScript

```javascript
fetch('http://localhost:8001/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Triệu chứng sốt?',
    conversation_history: [],
    use_rag: true
  })
})
.then(res => res.json())
.then(data => console.log(data.response));
```

---

## Bật Authentication (Tùy Chọn)

### 1. Tạo API Key

```bash
cd backend
python generate_api_key.py
```

### 2. Cập Nhật .env

```env
ENABLE_API_KEY_AUTH=true
API_KEYS=YOUR_GENERATED_KEY_HERE
```

### 3. Sử Dụng Khi Gọi API

```javascript
fetch('http://localhost:8001/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'YOUR_API_KEY'  // Thêm header này
  },
  body: JSON.stringify({
    message: 'Hello',
    conversation_history: [],
    use_rag: true
  })
});
```

---

## Các Endpoints Chính

| Endpoint | Method | Mô Tả |
|----------|--------|-------|
| `/` | GET | Thông tin API |
| `/api/info` | GET | Chi tiết cấu hình |
| `/health` | GET | Health check |
| `/chat` | POST | Chat cơ bản |
| `/chat/stream` | POST | Chat streaming (SSE) |
| `/documents/upload` | POST | Upload PDF |
| `/documents/stats` | GET | Thống kê documents |

---

## Tài Liệu Chi Tiết

Xem file [API_INTEGRATION.md](API_INTEGRATION.md) để biết:
- Cách cấu hình chi tiết
- Ví dụ code đầy đủ cho React, Vue, HTML
- Xử lý lỗi và retry logic
- Best practices
- Troubleshooting

---

## Swagger UI

Truy cập: **http://localhost:8001/docs**

Tại đây bạn có thể:
- Xem tất cả endpoints
- Test API trực tiếp
- Xem request/response schemas

---

## Files Mới Được Tạo

1. **`backend/auth.py`** - Module xác thực API key
2. **`backend/rate_limiter.py`** - Module giới hạn request
3. **`backend/generate_api_key.py`** - Script tạo API keys
4. **`backend/.env.example`** - Template cấu hình
5. **`API_INTEGRATION.md`** - Tài liệu tích hợp chi tiết
6. **`API_QUICK_START.md`** - Hướng dẫn nhanh (file này)

---

## Support

Nếu gặp vấn đề:

1. Kiểm tra logs của backend
2. Kiểm tra CORS settings trong `.env`
3. Kiểm tra API key (nếu bật authentication)
4. Test với `curl` trước khi tích hợp vào app

**Happy Coding! 🚀**
