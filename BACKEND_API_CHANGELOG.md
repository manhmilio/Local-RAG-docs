# 🎯 Cập Nhật Backend API - Changelog

## Ngày cập nhật: 2 tháng 1, 2026

---

## ✨ Tính Năng Mới

### 1. **API Key Authentication** 🔐
- Module xác thực với API key trong header `X-API-Key`
- Có thể bật/tắt linh hoạt qua `.env`
- Script tự động tạo API keys
- Hỗ trợ nhiều API keys cùng lúc

**Files:**
- `backend/auth.py` - Authentication module
- `backend/generate_api_key.py` - Script tạo keys

### 2. **Rate Limiting** ⏱️
- Giới hạn số requests per minute và per hour
- In-memory rate limiter (không cần database)
- Headers thông báo rate limit status
- Có thể tùy chỉnh limits qua `.env`

**Files:**
- `backend/rate_limiter.py` - Rate limiting module

### 3. **CORS Configuration Linh Hoạt** 🌐
- Cho phép tất cả origins (`ALLOW_ALL_ORIGINS=true`)
- Hoặc chỉ định danh sách cụ thể
- Expose rate limit headers

### 4. **API Information Endpoint** ℹ️
- Endpoint mới: `GET /api/info`
- Trả về thông tin về model, features, limits
- Hữu ích cho client kiểm tra cấu hình

### 5. **Enhanced Endpoints** 🚀
- Tất cả endpoints đều hỗ trợ authentication
- Rate limiting áp dụng cho chat endpoints
- Better error handling và status codes
- Detailed API documentation trong Swagger

---

## 📁 Files Mới

```
backend/
  ├── auth.py                    # Module xác thực API key
  ├── rate_limiter.py            # Module rate limiting
  ├── generate_api_key.py        # Script tạo API keys
  ├── test_api.py                # Script test các endpoints
  └── .env.example               # Template cấu hình

docs/
  ├── API_INTEGRATION.md         # Tài liệu chi tiết tích hợp API
  └── API_QUICK_START.md         # Hướng dẫn nhanh

examples/
  └── example_integration.html   # Demo HTML tích hợp API
```

---

## 🔧 Files Đã Cập Nhật

### `backend/config.py`
- Thêm `ENABLE_API_KEY_AUTH`
- Thêm `API_KEYS` với parser
- Thêm `ALLOW_ALL_ORIGINS`
- Thêm `ENABLE_RATE_LIMITING`
- Thêm `RATE_LIMIT_PER_MINUTE` và `RATE_LIMIT_PER_HOUR`

### `backend/main.py`
- Import auth và rate_limiter modules
- Cập nhật app description
- Expose rate limit headers trong CORS
- Cập nhật root endpoint với thông tin đầy đủ
- Thêm endpoint `/api/info`
- Thêm authentication cho endpoints nhạy cảm
- Thêm rate limiting cho chat endpoints

---

## 📝 Cấu Hình

### File `.env` Mẫu

```env
# CORS
ALLOW_ALL_ORIGINS=true
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Authentication (Optional)
ENABLE_API_KEY_AUTH=false
API_KEYS=

# Rate Limiting
ENABLE_RATE_LIMITING=true
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

---

## 🚀 Hướng Dẫn Sử Dụng

### Development Mode (Không Authentication)

1. **Tạo file `.env`:**
```bash
cd backend
cp .env.example .env
```

2. **Chỉnh sửa `.env`:**
```env
ALLOW_ALL_ORIGINS=true
ENABLE_API_KEY_AUTH=false
```

3. **Khởi động backend:**
```bash
python main.py
```

4. **Test API:**
```bash
python test_api.py
```

### Production Mode (Với Authentication)

1. **Tạo API keys:**
```bash
python generate_api_key.py
```

2. **Cập nhật `.env`:**
```env
ENABLE_API_KEY_AUTH=true
API_KEYS=your-generated-key-here
ALLOW_ALL_ORIGINS=false
CORS_ORIGINS=https://yourdomain.com
```

3. **Restart backend**

---

## 💻 Tích Hợp Vào Dự Án Khác

### JavaScript/React

```javascript
const API_URL = 'http://localhost:8001';
const API_KEY = 'your-api-key';  // Nếu cần

async function chat(message) {
  const response = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': API_KEY  // Thêm nếu bật auth
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

```vue
<script>
export default {
  data() {
    return {
      apiUrl: 'http://localhost:8001',
      apiKey: 'your-api-key'
    }
  },
  methods: {
    async sendMessage(message) {
      const response = await fetch(`${this.apiUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': this.apiKey
        },
        body: JSON.stringify({
          message,
          conversation_history: [],
          use_rag: true
        })
      });
      return await response.json();
    }
  }
}
</script>
```

Xem thêm ví dụ trong `API_INTEGRATION.md`

---

## 📚 Endpoints

| Endpoint | Method | Auth | Rate Limited | Mô Tả |
|----------|--------|------|--------------|-------|
| `/` | GET | ❌ | ❌ | API info |
| `/api/info` | GET | ❌ | ❌ | Detailed config |
| `/health` | GET | ❌ | ❌ | Health check |
| `/chat` | POST | Optional | ✅ | Chat cơ bản |
| `/chat/stream` | POST | Optional | ✅ | Chat streaming |
| `/documents/upload` | POST | ✅ | ❌ | Upload PDF |
| `/documents/stats` | GET | ❌ | ❌ | Documents stats |
| `/documents/reindex` | POST | ✅ | ❌ | Reindex all |

---

## 🧪 Testing

### Test với Script

```bash
cd backend
python test_api.py
```

### Test với cURL

```bash
# Test connection
curl http://localhost:8001/api/info

# Test chat
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "conversation_history": [], "use_rag": true}'

# Test with API key
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{"message": "Hello", "conversation_history": [], "use_rag": true}'
```

### Test với HTML Demo

Mở file `example_integration.html` trong browser:
1. Cấu hình API URL
2. (Optional) Nhập API key
3. Click "Test Connection"
4. Bắt đầu chat!

---

## 🎨 Demo Application

File `example_integration.html` là một demo hoàn chỉnh với:
- ✅ Giao diện đẹp, responsive
- ✅ Test connection
- ✅ Chat interface
- ✅ Hiển thị sources
- ✅ Typing indicator
- ✅ Error handling

Chỉ cần mở file HTML trong browser, không cần build hay install gì cả!

---

## 🔒 Security Best Practices

1. **API Keys:**
   - Không commit API keys vào git
   - Sử dụng environment variables
   - Rotate keys định kỳ

2. **CORS:**
   - Production: Chỉ định cụ thể origins
   - Development: Có thể dùng `ALLOW_ALL_ORIGINS=true`

3. **Rate Limiting:**
   - Luôn bật trong production
   - Adjust limits phù hợp với use case

---

## 📖 Documentation

- **Quick Start:** `API_QUICK_START.md`
- **Full Documentation:** `API_INTEGRATION.md`
- **Swagger UI:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc

---

## ⚠️ Troubleshooting

### CORS Errors
```env
# Solution 1: Allow all
ALLOW_ALL_ORIGINS=true

# Solution 2: Add your domain
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### 401 Unauthorized
- Kiểm tra API key có đúng không
- Kiểm tra `ENABLE_API_KEY_AUTH` setting
- Kiểm tra header `X-API-Key`

### 429 Rate Limit
- Đợi theo `Retry-After` header
- Tăng limits trong `.env`
- Hoặc tắt: `ENABLE_RATE_LIMITING=false`

---

## 🎯 Next Steps

1. Test API với `test_api.py`
2. Mở `example_integration.html` để xem demo
3. Đọc `API_INTEGRATION.md` để tích hợp vào dự án
4. Cấu hình authentication nếu cần
5. Deploy và enjoy! 🚀

---

## 📞 Support

Nếu có vấn đề:
1. Kiểm tra logs của backend
2. Test với `test_api.py`
3. Xem Swagger docs tại `/docs`
4. Đọc `API_INTEGRATION.md`

**Happy Coding! 🎉**
