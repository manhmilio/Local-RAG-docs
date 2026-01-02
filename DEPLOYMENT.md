# ✅ DEPLOYMENT CHECKLIST

## 🚀 Local Development Setup

### Prerequisites
- [x] Python 3.10 or higher installed
- [x] Node.js 18 or higher installed
- [x] Ollama installed and running
- [x] Git installed (optional)

### Backend Setup
```powershell
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Linux/Mac

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Setup environment
copy ..\.env.example .env

# 7. Test installation
python test_system.py

# 8. Start server
python main.py
```

✅ Backend running at: http://localhost:8000

### Frontend Setup
```powershell
# 1. Navigate to frontend (new terminal)
cd frontend

# 2. Install dependencies
npm install

# 3. Setup environment
copy .env.example .env

# 4. Start dev server
npm run dev
```

✅ Frontend running at: http://localhost:3000

### Ollama Setup
```powershell
# 1. Check Ollama is running
ollama list

# 2. Pull model (choose one)
ollama pull mistral:7b        # Recommended
# OR
ollama pull llama3.1:8b       # Alternative

# 3. Verify model
ollama list
```

---

## 🧪 Testing

### Backend Tests
```powershell
cd backend
python test_system.py
```

### API Health Check
```powershell
curl http://localhost:8000/health
```

### Manual Test Chat
```powershell
curl -X POST http://localhost:8000/chat `
  -H "Content-Type: application/json" `
  -d '{\"message\":\"Triệu chứng cảm cúm là gì?\",\"use_rag\":false}'
```

### Frontend Test
1. Open http://localhost:3000
2. Check health indicator (green = OK)
3. Try sample questions
4. Upload sample PDF
5. Test chat with RAG

---

## 📦 Production Deployment

### Environment Variables

**Backend (.env)**
```env
HOST=0.0.0.0
PORT=8000
OLLAMA_BASE_URL=http://ollama-server:11434
OLLAMA_MODEL=mistral:7b
CHROMA_PERSIST_DIRECTORY=/app/chroma_db
PDF_DATA_PATH=/app/data
TEMPERATURE=0.3
MAX_TOKENS=2048
TOP_K_RESULTS=3
SIMILARITY_THRESHOLD=0.7
CORS_ORIGINS=https://yourdomain.com
```

**Frontend (.env)**
```env
VITE_API_URL=https://api.yourdomain.com
```

### Build Frontend
```powershell
cd frontend
npm run build
# Output in dist/ folder
```

### Docker Deployment (Optional)

**docker-compose.yml**
```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./chroma_db:/app/chroma_db
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - ollama

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  ollama_data:
```

### Deployment Steps
1. Build images: `docker-compose build`
2. Start services: `docker-compose up -d`
3. Check logs: `docker-compose logs -f`
4. Pull model: `docker exec -it <container> ollama pull mistral:7b`

---

## 🔒 Security Checklist

### Pre-Production
- [ ] Change all default passwords
- [ ] Update CORS_ORIGINS to production domain
- [ ] Enable HTTPS (SSL/TLS)
- [ ] Set secure environment variables
- [ ] Add rate limiting
- [ ] Implement authentication
- [ ] Setup API keys
- [ ] Enable request logging
- [ ] Add input validation
- [ ] Setup backup strategy

### Monitoring
- [ ] Setup health checks
- [ ] Configure alerting
- [ ] Enable error tracking (Sentry)
- [ ] Monitor resource usage
- [ ] Track API metrics
- [ ] Log analysis setup

---

## 🔄 Maintenance

### Daily
- [ ] Check health status
- [ ] Monitor error logs
- [ ] Review API usage

### Weekly
- [ ] Update dependencies
- [ ] Review security patches
- [ ] Backup database
- [ ] Clean old logs

### Monthly
- [ ] Update models
- [ ] Optimize database
- [ ] Review performance
- [ ] Update documentation

---

## 📊 Performance Optimization

### Backend
```python
# 1. Reduce chunk size if memory issues
chunk_size = 500  # Default: 1000

# 2. Optimize embeddings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Faster

# 3. Limit max tokens
MAX_TOKENS = 1024  # Default: 2048

# 4. Reduce top-k results
TOP_K_RESULTS = 2  # Default: 3
```

### Frontend
```javascript
// 1. Enable production build
npm run build

// 2. Use CDN for assets
// 3. Enable caching
// 4. Optimize images
// 5. Code splitting
```

### Database
```python
# 1. Periodic cleanup
vs.delete_old_documents(days=30)

# 2. Optimize collection
vs.optimize_collection()

# 3. Backup regularly
vs.backup_collection()
```

---

## 🆘 Emergency Procedures

### Backend Down
1. Check Ollama: `ollama list`
2. Restart backend: `systemctl restart backend`
3. Check logs: `tail -f logs/backend.log`
4. Verify ChromaDB: `ls chroma_db/`

### Frontend Down
1. Check backend API: `curl http://backend:8000/health`
2. Restart frontend: `systemctl restart frontend`
3. Clear browser cache
4. Check CORS settings

### Database Issues
1. Backup: `cp -r chroma_db chroma_db.backup`
2. Reset: `rm -rf chroma_db`
3. Restart backend (recreates DB)
4. Reindex: `curl -X POST /documents/reindex`

### Model Issues
1. Check Ollama: `ollama ps`
2. Pull model again: `ollama pull mistral:7b`
3. Switch model in .env
4. Restart services

---

## 📞 Support Contacts

**Technical Issues:**
- GitHub Issues: [link]
- Email: support@example.com

**Documentation:**
- README.md
- API Docs: http://localhost:8000/docs

**Community:**
- Discord: [link]
- Forum: [link]

---

## 📝 Notes

- Always backup before major changes
- Test in staging before production
- Keep dependencies updated
- Monitor resource usage
- Document all changes
- Follow security best practices

---

**Last Updated:** January 2026
**Version:** 1.0.0
