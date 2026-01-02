# 🚀 QUICK START GUIDE

## Khởi Động Nhanh Trong 5 Phút

### 1. Cài Đặt Ollama

```powershell
# Download và cài đặt từ: https://ollama.ai/download
# Sau khi cài, pull model:
ollama pull mistral:7b
```

### 2. Setup Backend

```powershell
cd backend

# Tạo virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy ..\.env.example .env

# Chạy server
python main.py
```

✅ Backend sẽ chạy tại: http://localhost:8000

### 3. Setup Frontend (Terminal mới)

```powershell
cd frontend

# Install dependencies
npm install

# Copy environment file
copy .env.example .env

# Chạy dev server
npm run dev
```

✅ Frontend sẽ chạy tại: http://localhost:3000

### 4. Sử Dụng

1. Mở browser: http://localhost:3000
2. Upload tài liệu PDF y tế (optional)
3. Bắt đầu chat!

---

## 🔍 Kiểm Tra Hệ Thống

### Backend Health Check
```powershell
curl http://localhost:8000/health
```

### Ollama Status
```powershell
ollama list
```

### Test API
```powershell
curl -X POST http://localhost:8000/chat `
  -H "Content-Type: application/json" `
  -d '{"message":"Xin chào","use_rag":false}'
```

---

## 📦 Sample Data

Tạo file PDF mẫu trong thư mục `data/`:
```
data/
├── medical_guide.pdf
├── disease_symptoms.pdf
└── treatment_protocols.pdf
```

Sau đó reindex:
```powershell
curl -X POST http://localhost:8000/documents/reindex
```

---

## ⚠️ Common Issues

**Ollama not running?**
```powershell
# Windows: Mở Ollama app từ Start Menu
# Hoặc restart service
```

**Port already in use?**
```powershell
# Đổi port trong .env
PORT=8001
```

**Module not found?**
```powershell
# Backend
pip install --force-reinstall -r requirements.txt

# Frontend
rm -r node_modules
npm install
```

---

## 📖 Full Documentation

Xem [README.md](README.md) để biết chi tiết đầy đủ.
