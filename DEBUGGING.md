# 🐛 Debugging Guide

## Common Problems & Solutions

### 1. Backend Won't Start

#### Error: "Module not found"
```powershell
# Solution: Reinstall dependencies
cd backend
pip install --force-reinstall -r requirements.txt
```

#### Error: "Address already in use (port 8000)"
```powershell
# Solution 1: Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Solution 2: Change port in .env
PORT=8001
```

#### Error: "Connection to Ollama failed"
```powershell
# Check Ollama status
ollama list

# Restart Ollama
# Windows: Close and reopen Ollama app
# Linux/Mac: systemctl restart ollama

# Test connection
curl http://localhost:11434/api/tags
```

### 2. Frontend Won't Start

#### Error: "npm ERR! missing script: dev"
```powershell
# Solution: Make sure you're in frontend folder
cd frontend
npm install
```

#### Error: "Port 3000 already in use"
```powershell
# Solution 1: Kill process
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Solution 2: Use different port
npm run dev -- --port 3001
```

#### Error: "Failed to fetch" in browser
```javascript
// Solution: Check CORS and backend URL
// In frontend/.env
VITE_API_URL=http://localhost:8000

// Check backend CORS in .env
CORS_ORIGINS=http://localhost:3000
```

### 3. ChromaDB Issues

#### Error: "Collection not found"
```powershell
# Solution: Reset ChromaDB
rm -r chroma_db
# Restart backend - will recreate automatically
```

#### Error: "Database is locked"
```powershell
# Solution: Kill all Python processes
taskkill /F /IM python.exe
# Restart backend
```

### 4. PDF Processing Issues

#### Error: "Can't extract text from PDF"
```python
# Possible causes:
# 1. PDF is image-based (scanned) - needs OCR
# 2. PDF is encrypted
# 3. PDF is corrupted

# Solution: Use text-based PDFs only
# For scanned PDFs, use OCR tools first
```

#### Error: "No chunks created"
```python
# Possible cause: PDF too short or empty
# Solution: Check PDF has actual text content
```

### 5. Embedding Issues

#### Error: "Failed to create embeddings"
```powershell
# Solution: Model might be downloading
# Wait for sentence-transformers to finish downloading
# Check: ~/.cache/torch/sentence_transformers/
```

#### Error: "Out of memory"
```python
# Solution: Reduce chunk size or batch size
# In pdf_processor.py:
self.chunk_size = 500  # Reduce from 1000
```

### 6. LLM Generation Issues

#### Error: "Model not found"
```powershell
# Solution: Pull the model
ollama pull mistral:7b

# Check available models
ollama list
```

#### Error: "Response too slow"
```env
# Solution: Reduce max tokens
MAX_TOKENS=1024  # Reduce from 2048

# Or use smaller model
OLLAMA_MODEL=mistral:7b  # Instead of llama3.1:70b
```

#### Error: "Response in wrong language"
```python
# Solution: Adjust system prompt in llm_service.py
# Add: "Luôn trả lời bằng tiếng Việt"
```

### 7. Streaming Issues

#### Error: "Stream stops midway"
```javascript
// Solution: Check network timeout
// In api.js, add timeout config
const response = await fetch(url, {
  ...config,
  signal: AbortSignal.timeout(60000) // 60s timeout
});
```

#### Error: "Stream not working"
```javascript
// Solution: Check browser supports SSE
// Try in Chrome/Firefox
// Check browser console for errors
```

### 8. Database/Vector Store Issues

#### Error: "Similarity search returns nothing"
```python
# Possible causes:
# 1. No documents in database
# 2. Threshold too high
# 3. Embedding mismatch

# Solution 1: Check document count
curl http://localhost:8000/documents/stats

# Solution 2: Lower threshold
SIMILARITY_THRESHOLD=0.5  # From 0.7

# Solution 3: Reindex documents
curl -X POST http://localhost:8000/documents/reindex
```

---

## Logging & Debugging

### Enable Debug Logging

```python
# In backend/main.py or config.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### View Backend Logs

```powershell
# Real-time logs
python main.py

# Save to file
python main.py > logs.txt 2>&1
```

### View Frontend Logs

```javascript
// Open browser console (F12)
// Check Network tab for API calls
// Check Console tab for JavaScript errors
```

### Database Inspection

```python
# In Python shell
from vector_store import VectorStore
vs = VectorStore()
stats = vs.get_stats()
print(stats)
```

---

## Performance Debugging

### Slow Responses

1. **Profile LLM:**
```python
import time
start = time.time()
response = await llm.generate_response(query)
print(f"Time: {time.time() - start}s")
```

2. **Profile Vector Search:**
```python
start = time.time()
docs = vs.similarity_search(query)
print(f"Search time: {time.time() - start}s")
```

3. **Optimize Settings:**
```env
# Reduce tokens
MAX_TOKENS=1024

# Reduce search results
TOP_K_RESULTS=2

# Use faster model
OLLAMA_MODEL=mistral:7b
```

---

## Testing Commands

### Test Backend Health
```powershell
curl http://localhost:8000/health
```

### Test Chat Endpoint
```powershell
curl -X POST http://localhost:8000/chat `
  -H "Content-Type: application/json" `
  -d '{\"message\":\"Hello\",\"use_rag\":false}'
```

### Test Vector Search
```python
from vector_store import VectorStore
vs = VectorStore()
docs, metas, scores = vs.similarity_search("test query")
print(f"Found {len(docs)} documents")
```

### Run System Tests
```powershell
cd backend
python test_system.py
```

---

## Need More Help?

1. Check GitHub Issues
2. Enable debug logging
3. Run test_system.py
4. Check Ollama logs
5. Check browser console
6. Contact support with logs

---

## Useful Commands

```powershell
# Check processes
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Kill Python
taskkill /F /IM python.exe

# Kill Node
taskkill /F /IM node.exe

# Check disk space
dir chroma_db

# Check Python packages
pip list

# Check Node packages
npm list
```
