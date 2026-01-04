# 🎯 GETTING STARTED

Chào mừng bạn đến với Medical Chatbot! Hướng dẫn này sẽ giúp bạn chạy được hệ thống trong 10 phút.

---

## 📋 Bước 1: Kiểm Tra Yêu Cầu Hệ Thống

### Cần Có
✅ **Python 3.10+**
```powershell
python --version
# Nếu chưa có: Download từ https://www.python.org/downloads/
```

✅ **Node.js 18+**
```powershell
node --version
# Nếu chưa có: Download từ https://nodejs.org/
```

✅ **Ollama**
```powershell
ollama --version
# Nếu chưa có: Download từ https://ollama.ai/download
```

### Kiểm Tra Disk Space
- Backend dependencies: ~500 MB
- Frontend dependencies: ~300 MB
- Ollama model: ~4-5 GB
- **Tổng cộng: ~6 GB**

---

## 🚀 Bước 2: Cài Đặt Ollama và Model

### Windows

1. **Download Ollama:**
   - Truy cập: https://ollama.ai/download
   - Download và cài đặt Ollama for Windows

2. **Khởi động Ollama:**
   - Ollama sẽ tự chạy sau khi cài
   - Kiểm tra: Tìm icon Ollama ở system tray

3. **Pull Model:**
```powershell
# Mở PowerShell và chạy:
ollama pull mistral:7b

# Chờ download (4-5 GB, mất 5-10 phút)
# Kiểm tra:
ollama list
```

### Linux/Mac
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull model
ollama pull mistral:7b

# Verify
ollama list
```

---

## 🔧 Bước 3: Setup Backend

### 3.1. Mở Terminal và Navigate

```powershell
cd D:\ML\Local-RAG\backend
```

### 3.2. Tạo Virtual Environment

```powershell
# Tạo venv
python -m venv venv

# Kích hoạt (QUAN TRỌNG!)
.\venv\Scripts\Activate.ps1

# Nếu gặp lỗi ExecutionPolicy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Kiểm tra: prompt sẽ có (venv) ở đầu
```

### 3.3. Install Dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install packages (mất 2-3 phút)
pip install -r requirements.txt
```

**⏳ Chờ cài đặt... Đây là lúc tốt để pha cà phê!**

### 3.4. Kiểm Tra Installation

```powershell
# Test system
python test_system.py

# Kết quả mong đợi:
# ✅ VectorStore: PASS
# ✅ LLM Service: PASS
# ✅ PDF Processor: PASS
# ✅ End-to-End: PASS
```

### 3.5. Khởi Động Backend

```powershell
python main.py

# Output mong đợi:
# 🚀 Khởi động ứng dụng Medical Chatbot...
# ✅ ChromaDB initialized
# ✅ Ollama connection OK
# ✅ Khởi động thành công!
# INFO: Uvicorn running on http://0.0.0.0:8000
```

**🎉 Backend đã sẵn sàng!** Để terminal này chạy và mở terminal mới.

---

## 🎨 Bước 4: Setup Frontend

### 4.1. Mở Terminal Mới

```powershell
# Navigate đến frontend
cd D:\ML\Local-RAG\frontend
```

### 4.2. Install Dependencies

```powershell
# Install npm packages (mất 1-2 phút)
npm install
```

### 4.3. Khởi Động Frontend

```powershell
npm run dev

# Output mong đợi:
#   VITE v5.0.8  ready in 1234 ms
#
#   ➜  Local:   http://localhost:3000/
#   ➜  Network: use --host to expose
```

**🎉 Frontend đã sẵn sàng!**

---

## 🌐 Bước 5: Truy Cập Ứng Dụng

### Mở Browser

Truy cập: **http://localhost:3000**

Bạn sẽ thấy:
- ✅ Header với "Medical Chatbot" 
- ✅ Status indicator màu xanh "Đang hoạt động"
- ✅ Welcome message
- ✅ Sample questions để click

### Kiểm Tra API Docs

Truy cập: **http://localhost:8000/docs**

Bạn sẽ thấy Swagger UI với tất cả endpoints.

---

## 💬 Bước 6: Test Chatbot

### Test 1: Chat Đơn Giản (Không RAG)

1. Click vào sample question: **"Triệu chứng của bệnh cảm cúm là gì?"**
2. Chờ response streaming
3. Xem câu trả lời xuất hiện từng chữ

### Test 2: Upload Document

1. Click nút **"Upload PDF"** ở header
2. Chọn một file PDF y tế (hoặc tạo file test)
3. Upload và chờ processing
4. Xem message: "Đã xử lý thành công X chunks"

### Test 3: Chat Với RAG

1. Gõ câu hỏi liên quan đến document vừa upload
2. Xem response có **"📚 Nguồn tham khảo"** ở đầu
3. Kiểm tra nguồn được cite

---

## 🎊 Hoàn Thành!

Bạn đã setup thành công! Bây giờ bạn có:

✅ Backend API running (port 8000)  
✅ Frontend UI running (port 3000)  
✅ Ollama model ready  
✅ ChromaDB initialized  
✅ Chat interface working  
✅ RAG pipeline functional  

---

## 🎯 Các Bước Tiếp Theo

### 1. Thêm Tài Liệu Y Tế

Copy PDF files vào folder `data/`:
```powershell
copy medical_books.pdf D:\ML\Local-RAG\data\
```

Sau đó reindex:
```powershell
curl -X POST http://localhost:8000/documents/reindex
```

### 2. Tùy Chỉnh Model

Trong `backend\.env`:
```env
# Thử model khác
OLLAMA_MODEL=llama3.1:8b

# Điều chỉnh parameters
TEMPERATURE=0.5      # Sáng tạo hơn
MAX_TOKENS=4096      # Response dài hơn
```

Restart backend để áp dụng.

### 3. Customize UI

Trong `frontend\src\components\`:
- `Header.jsx` - Đổi title, logo
- `App.jsx` - Thêm features
- `index.css` - Đổi colors, styles

### 4. Deploy Production

Xem [DEPLOYMENT.md](DEPLOYMENT.md) để biết chi tiết.

---

## 🆘 Gặp Vấn Đề?

### Backend Không Start

```powershell
# Check Ollama
ollama list

# Check port
netstat -ano | findstr :8000

# View logs
python main.py 2>&1 | tee logs.txt
```

### Frontend Không Start

```powershell
# Clear cache
rm -r node_modules
npm install

# Check backend
curl http://localhost:8000/health
```

### Chat Không Hoạt Động

1. **Check browser console (F12)**
   - Có lỗi CORS?
   - API connection failed?

2. **Check backend logs**
   - Ollama connected?
   - Model loaded?

3. **Test API directly**
   ```powershell
   curl -X POST http://localhost:8000/chat `
     -H "Content-Type: application/json" `
     -d '{\"message\":\"test\",\"use_rag\":false}'
   ```

### Đọc Thêm

- [DEBUGGING.md](DEBUGGING.md) - Troubleshooting guide
- [README.md](README.md) - Full documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick reference

---

## 📞 Cần Trợ Giúp?

**Documentation:**
- README.md - Full docs
- API Docs - http://localhost:8000/docs

**Community:**
- GitHub Issues
- Discord (coming soon)

**Quick Commands:**
```powershell
# Start everything
.\start.bat              # Windows
./start.sh               # Linux/Mac

# Check health
curl http://localhost:8000/health

# View logs
Get-Content logs.txt -Tail 50
```

---

## 🎓 Learning More

**Ollama:**
- Models: https://ollama.ai/library
- Docs: https://github.com/ollama/ollama

**FastAPI:**
- Tutorial: https://fastapi.tiangolo.com/tutorial/

**React:**
- Learn: https://react.dev/learn

**RAG:**
- Guide: https://www.pinecone.io/learn/retrieval-augmented-generation/

---

**Chúc bạn code vui vẻ! 🚀**