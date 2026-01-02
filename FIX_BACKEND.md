# 🔧 Hướng Dẫn Sửa Lỗi Backend

## ❌ Lỗi hiện tại

```
KeyboardInterrupt khi import sympy/transformers
Nguyên nhân: Python 3.13 chưa tương thích hoàn toàn với một số packages
```

## ✅ Giải pháp 1: Downgrade Python (Khuyến nghị)

### Bước 1: Cài đặt Python 3.11 hoặc 3.12

**Download Python 3.11.9:**
- Link: https://www.python.org/downloads/release/python-3119/
- Chọn: **Windows installer (64-bit)**
- Cài đặt và **QUAN TRỌNG**: ✅ Tick "Add Python to PATH"

**Hoặc Python 3.12.7:**
- Link: https://www.python.org/downloads/release/python-3127/

### Bước 2: Xác minh cài đặt

```powershell
# Kiểm tra Python version (phải là 3.11.x hoặc 3.12.x)
python --version

# Nếu vẫn hiện 3.13, dùng py launcher:
py -3.11 --version
# hoặc
py -3.12 --version
```

### Bước 3: Tạo lại Virtual Environment

```powershell
cd D:\ML\Local-RAG

# Xóa venv cũ (đã xóa rồi)
# Remove-Item -Recurse -Force venv

# Tạo venv mới với Python 3.11/3.12
# Cách 1: Nếu Python 3.11 là default
python -m venv venv

# Cách 2: Nếu có nhiều Python, dùng py launcher
py -3.11 -m venv venv
# hoặc
py -3.12 -m venv venv
```

### Bước 4: Activate và cài đặt packages

```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Cài đặt dependencies
pip install -r backend\requirements.txt
```

### Bước 5: Test hệ thống

```powershell
# Chạy tests
python backend\test_system.py

# Nếu tests PASS, khởi động backend
python backend\main.py
```

Backend sẽ chạy tại: **http://localhost:8000**

---

## ✅ Giải pháp 2: Sử dụng Conda (Thay thế)

```powershell
# Cài Miniconda: https://docs.conda.io/en/latest/miniconda.html

# Tạo environment với Python 3.11
conda create -n medical-chatbot python=3.11 -y

# Activate
conda activate medical-chatbot

# Cài packages
cd D:\ML\Local-RAG
pip install -r backend\requirements.txt

# Test
python backend\test_system.py
```

---

## ✅ Giải pháp 3: Docker (Advanced)

```powershell
# Tạo Dockerfile
cd D:\ML\Local-RAG\backend
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

```powershell
# Build và run
docker build -t medical-chatbot .
docker run -p 8000:8000 medical-chatbot
```

---

## 🎯 Sau khi sửa xong

### Kiểm tra Backend hoạt động:

```powershell
# Terminal 1: Chạy backend
cd D:\ML\Local-RAG
.\venv\Scripts\Activate.ps1
python backend\main.py
```

### Frontend đã chạy rồi tại http://localhost:3000

Refresh trang web và test chat!

---

## 📝 Troubleshooting

### Lỗi: "python không được nhận dạng"
```powershell
# Thêm Python vào PATH hoặc dùng đường dẫn đầy đủ
C:\Python311\python.exe -m venv venv
```

### Lỗi: "Activate.ps1 cannot be loaded"
```powershell
# Cho phép chạy scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Lỗi: Packages vẫn fail
```powershell
# Cài từng nhóm packages
pip install fastapi uvicorn pydantic
pip install langchain langchain-community
pip install chromadb sentence-transformers
pip install ollama torch
```

---

## 📞 Cần trợ giúp?

1. **Backend tests PASS** = Code hoàn toàn OK
2. Chỉ là vấn đề **tương thích Python version**
3. Python 3.11 hoặc 3.12 sẽ hoạt động **100%**

**Sau khi fix xong, hệ thống sẽ hoạt động như sau:**
- ✅ Backend: http://localhost:8000
- ✅ Frontend: http://localhost:3000 (đang chạy)
- ✅ Chat với AI medical assistant
- ✅ Upload PDF documents
- ✅ RAG system với ChromaDB + Ollama
