# 🏥 Medical Chatbot - Hệ Thống Chẩn Đoán Bệnh AI

Hệ thống chatbot y tế thông minh sử dụng RAG (Retrieval Augmented Generation) với Ollama LLM và ChromaDB vector store.

## 📋 Tổng Quan

### Công Nghệ Stack

**Backend:**
- FastAPI 0.104+ (Python 3.10+)
- Ollama (mistral:7b hoặc llama3.1:8b)
- ChromaDB (Vector Database)
- LangChain Framework
- Sentence-Transformers (Embeddings)
- PyPDF2 (PDF Processing)

**Frontend:**
- React 18+
- Tailwind CSS 3+
- Vite (Build Tool)
- Axios (HTTP Client)
- React Markdown (Markdown Rendering)
- Lucide React (Icons)

### Tính Năng Chính

✅ Chat interface hiện đại với streaming responses  
✅ RAG system với ChromaDB vector search  
✅ Upload và xử lý tài liệu PDF y tế  
✅ Hỗ trợ tiếng Việt tốt  
✅ Semantic search với embeddings multilingual  
✅ Real-time health check và monitoring  
✅ Lưu trữ lịch sử chat  
✅ Markdown formatting cho responses  

---

## 🚀 Hướng Dẫn Cài Đặt

### Bước 1: Cài Đặt Ollama

#### Windows:
1. Download Ollama từ: https://ollama.ai/download
2. Chạy installer và cài đặt
3. Mở PowerShell và pull model:

```powershell
ollama pull mistral:7b
# Hoặc
ollama pull llama3.1:8b
```

4. Kiểm tra Ollama đang chạy:
```powershell
ollama list
```

#### Linux/Mac:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull mistral:7b
```

### Bước 2: Setup Backend

1. **Tạo Python Virtual Environment:**

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Linux/Mac
```

2. **Cài đặt Dependencies:**

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

3. **Cấu hình Environment Variables:**

```powershell
# Copy file .env.example
copy ..\.env.example .env

# Chỉnh sửa .env nếu cần (mặc định đã OK cho local)
```

4. **Khởi động Backend Server:**

```powershell
python main.py
```

Server sẽ chạy tại: http://localhost:8000  
API Docs: http://localhost:8000/docs

### Bước 3: Setup Frontend

1. **Cài đặt Node.js Dependencies:**

```powershell
cd ..\frontend
npm install
```

2. **Cấu hình Environment:**

```powershell
copy .env.example .env
```

3. **Khởi động Development Server:**

```powershell
npm run dev
```

Frontend sẽ chạy tại: http://localhost:3000

---

## 📁 Cấu Trúc Dự Án

```
Local-RAG/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic data models
│   ├── vector_store.py      # ChromaDB integration
│   ├── llm_service.py       # Ollama LLM service
│   ├── pdf_processor.py     # PDF processing module
│   └── requirements.txt     # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── ChatMessage.jsx
│   │   │   ├── ChatInput.jsx
│   │   │   ├── Header.jsx
│   │   │   ├── TypingIndicator.jsx
│   │   │   └── UploadModal.jsx
│   │   ├── services/
│   │   │   └── api.js       # API service
│   │   ├── App.jsx          # Main app component
│   │   ├── main.jsx         # Entry point
│   │   └── index.css        # Global styles
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── data/                    # PDF documents folder
├── chroma_db/              # ChromaDB persistent storage
└── .env.example            # Environment variables template
```

---

## 🔧 Cấu Hình Chi Tiết

### Backend Configuration (.env)

```env
# Server
HOST=0.0.0.0
PORT=8000
RELOAD=True

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b

# ChromaDB
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_COLLECTION_NAME=medical_documents

# Embeddings
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2

# LLM Parameters
TEMPERATURE=0.3          # Độ sáng tạo (0-1)
MAX_TOKENS=2048          # Max tokens response
TOP_P=0.9               # Nucleus sampling

# RAG Settings
TOP_K_RESULTS=3          # Số documents retrieve
SIMILARITY_THRESHOLD=0.7 # Ngưỡng similarity

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend Configuration (.env)

```env
VITE_API_URL=http://localhost:8000
```

---

## 📚 Sử Dụng

### 1. Upload Tài Liệu PDF

1. Click nút "Upload PDF" trên header
2. Chọn file PDF y tế (sách, bài báo, tài liệu chẩn đoán...)
3. Hệ thống sẽ tự động:
   - Extract text từ PDF
   - Chia thành chunks
   - Tạo embeddings
   - Lưu vào ChromaDB

### 2. Chat với AI

1. Gõ câu hỏi vào ô input
2. Hệ thống sẽ:
   - Tìm kiếm documents liên quan (RAG)
   - Gửi context + question đến LLM
   - Stream response real-time
3. Xem nguồn tham khảo được hiển thị cùng câu trả lời

### 3. API Endpoints

#### Health Check
```bash
GET /health
```

#### Chat (Non-streaming)
```bash
POST /chat
Content-Type: application/json

{
  "message": "Triệu chứng của bệnh cảm cúm là gì?",
  "use_rag": true,
  "conversation_history": []
}
```

#### Chat (Streaming)
```bash
POST /chat/stream
Content-Type: application/json

{
  "message": "Triệu chứng của bệnh cảm cúm là gì?",
  "use_rag": true
}
```

#### Upload Document
```bash
POST /documents/upload
Content-Type: multipart/form-data

file: <PDF_FILE>
```

#### Get Stats
```bash
GET /documents/stats
```

#### Reindex All PDFs
```bash
POST /documents/reindex
```

---

## 🛠️ Troubleshooting

### Backend Issues

**Problem: "Connection to Ollama failed"**
```powershell
# Kiểm tra Ollama service
ollama list

# Restart Ollama (Windows)
# Tắt và mở lại Ollama app

# Test connection
curl http://localhost:11434/api/tags
```

**Problem: "ChromaDB error"**
```powershell
# Xóa và tạo lại database
rm -r chroma_db
# Restart backend - sẽ tự tạo lại
```

**Problem: "Model not found"**
```powershell
# Pull model
ollama pull mistral:7b
```

**Problem: "Import errors"**
```powershell
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Frontend Issues

**Problem: "API connection failed"**
- Kiểm tra backend đang chạy tại port 8000
- Kiểm tra CORS settings
- Xem console logs

**Problem: "Module not found"**
```powershell
# Clear cache và reinstall
rm -r node_modules
rm package-lock.json
npm install
```

**Problem: "Build errors"**
```powershell
npm run build
# Check console for specific errors
```

---

## 🎯 Tối Ưu Hiệu Suất

### 1. LLM Parameters

Chỉnh sửa trong `.env`:
```env
TEMPERATURE=0.3      # ↓ = chính xác hơn, ↑ = sáng tạo hơn
MAX_TOKENS=2048      # Tăng cho responses dài hơn
TOP_P=0.9           # Nucleus sampling
```

### 2. RAG Settings

```env
TOP_K_RESULTS=3              # Số documents retrieve
SIMILARITY_THRESHOLD=0.7     # Ngưỡng minimum similarity
```

### 3. Chunking Strategy

Trong `pdf_processor.py`:
```python
self.chunk_size = 1000       # Kích thước chunk
self.chunk_overlap = 200     # Overlap giữa chunks
```

### 4. Embedding Model

Có thể thay đổi model trong `.env`:
```env
# Faster but less accurate
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Better for Vietnamese
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2

# Best quality (slower)
EMBEDDING_MODEL=paraphrase-multilingual-mpnet-base-v2
```

---

## 🔒 Production Deployment

### 1. Security Checklist

- [ ] Thay đổi CORS origins
- [ ] Thêm authentication/authorization
- [ ] Rate limiting
- [ ] Input validation & sanitization
- [ ] HTTPS only
- [ ] Environment variables từ secrets manager

### 2. Docker Deployment

#### Backend Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Dockerfile
```dockerfile
FROM node:18-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./chroma_db:/app/chroma_db
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:11434

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
```

### 3. Monitoring

Thêm logging và metrics:
```python
# backend/main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

---

## 📊 Performance Benchmarks

### Expected Performance

- **Embedding generation**: ~50ms per chunk
- **Vector search**: ~10-30ms for 1000 documents
- **LLM response (streaming)**: First token ~500ms, subsequent ~50ms/token
- **PDF processing**: ~2-5s per page

### Scaling Recommendations

- **< 1000 documents**: Current setup OK
- **1000-10000 documents**: Consider Postgres with pgvector
- **> 10000 documents**: Use Pinecone/Weaviate/Qdrant
- **High traffic**: Add load balancer, multiple Ollama instances

---

## 🤝 Contributing

### Development Setup

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes
4. Test thoroughly
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Create Pull Request

### Code Style

- Python: Follow PEP 8
- JavaScript: ESLint config included
- Comments: Tiếng Việt cho business logic

---

## 📝 License

MIT License - xem file LICENSE

---

## 🆘 Support

**Issues**: Create issue trên GitHub  
**Discussions**: GitHub Discussions  
**Email**: support@example.com

---

## 🙏 Credits

- **Ollama**: https://ollama.ai
- **LangChain**: https://langchain.com
- **ChromaDB**: https://www.trychroma.com
- **FastAPI**: https://fastapi.tiangolo.com
- **React**: https://react.dev

---

## 📅 Roadmap

- [ ] User authentication & authorization
- [ ] Multi-user support với isolated vector stores
- [ ] Advanced medical NER (Named Entity Recognition)
- [ ] Integration với medical databases (ICD-10, SNOMED)
- [ ] Voice input/output
- [ ] Mobile app (React Native)
- [ ] Multilingual support (English, Vietnamese, etc.)
- [ ] A/B testing different LLM models
- [ ] Analytics dashboard
- [ ] Export chat history

---

**Version**: 1.0.0  
**Last Updated**: January 2026  
**Author**: Medical AI Team
