# 📝 CHEAT SHEET - Quick Commands Reference

## 🚀 Startup Commands

### Quick Start (Both Services)
```powershell
# Windows
.\start.bat

# Linux/Mac
./start.sh
```

### Backend Only
```powershell
cd backend
.\venv\Scripts\Activate.ps1  # Activate venv
python main.py                # Start server
```

### Frontend Only
```powershell
cd frontend
npm run dev                   # Start dev server
```

---

## 🔧 Installation Commands

### Backend Setup
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

### Frontend Setup
```powershell
cd frontend
npm install
```

### Ollama Setup
```powershell
ollama pull mistral:7b        # Download model
ollama list                   # List models
ollama ps                     # Running models
```

---

## 🧪 Testing Commands

### System Test
```powershell
cd backend
python test_system.py
```

### Health Check
```powershell
curl http://localhost:8000/health
```

### API Test
```powershell
# Simple chat
curl -X POST http://localhost:8000/chat `
  -H "Content-Type: application/json" `
  -d '{\"message\":\"Hello\",\"use_rag\":false}'

# Get stats
curl http://localhost:8000/documents/stats

# Reindex
curl -X POST http://localhost:8000/documents/reindex
```

---

## 🛠️ Ollama Management

### Model Operations
```powershell
# List installed models
ollama list

# Pull new model
ollama pull llama3.1:8b

# Delete model
ollama rm mistral:7b

# Show model info
ollama show mistral:7b

# Test model
ollama run mistral:7b "Test message"
```

### Using Model Manager
```powershell
cd backend
python ollama_manager.py list        # List models
python ollama_manager.py recommend   # Show recommendations
python ollama_manager.py pull <model>
python ollama_manager.py delete <model>
```

---

## 📊 Database Commands

### ChromaDB Operations
```python
# In Python shell
from vector_store import VectorStore

vs = VectorStore()
vs.get_stats()                # Get statistics
vs.similarity_search("query") # Test search
vs.delete_collection()        # Reset database
```

### Backup/Restore
```powershell
# Backup
xcopy /E /I chroma_db chroma_db_backup

# Restore
xcopy /E /I chroma_db_backup chroma_db

# Clean
rmdir /S /Q chroma_db
```

---

## 🐛 Debugging Commands

### Check Processes
```powershell
# Check ports
netstat -ano | findstr :8000    # Backend
netstat -ano | findstr :3000    # Frontend
netstat -ano | findstr :11434   # Ollama

# Kill process by port
$port = 8000
$processId = (Get-NetTCPConnection -LocalPort $port).OwningProcess
Stop-Process -Id $processId -Force
```

### View Logs
```powershell
# Backend logs (if redirected)
Get-Content logs.txt -Tail 50 -Wait

# View in real-time
python main.py 2>&1 | Tee-Object logs.txt
```

### Check Dependencies
```powershell
# Python packages
pip list
pip show <package>

# Node packages
npm list
npm list --depth=0
```

---

## 🔄 Update Commands

### Update Dependencies
```powershell
# Backend
cd backend
pip install --upgrade -r requirements.txt

# Frontend
cd frontend
npm update
```

### Update Models
```powershell
ollama pull mistral:7b          # Re-pull to update
```

---

## 🔒 Environment Commands

### View Environment
```powershell
# Show current config
cd backend
python -c "from config import settings; print(settings.dict())"
```

### Change Model
```powershell
# Edit .env
notepad backend\.env

# Change OLLAMA_MODEL line
# Restart backend
```

---

## 📦 Build Commands

### Frontend Production Build
```powershell
cd frontend
npm run build                    # Build for production
npm run preview                  # Preview build
```

### Clean Build
```powershell
# Frontend
rm -r frontend/dist
rm -r frontend/node_modules
npm install
npm run build

# Backend
rm -r backend/__pycache__
rm -r backend/**/__pycache__
```

---

## 🐳 Docker Commands (Optional)

### Build and Run
```powershell
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Container Management
```powershell
# List containers
docker ps

# Enter container
docker exec -it <container> bash

# View logs
docker logs <container> -f
```

---

## 📝 Git Commands (Optional)

### Initialize Repository
```powershell
git init
git add .
git commit -m "Initial commit"
git remote add origin <url>
git push -u origin main
```

### Update Repository
```powershell
git status
git add .
git commit -m "Update message"
git push
```

---

## 🎯 Quick Fixes

### Backend Won't Start
```powershell
# 1. Check Ollama
ollama list

# 2. Kill port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# 3. Reinstall deps
pip install --force-reinstall -r requirements.txt

# 4. Reset ChromaDB
rmdir /S /Q chroma_db
```

### Frontend Won't Start
```powershell
# 1. Kill port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# 2. Clean install
rmdir /S /Q node_modules
del package-lock.json
npm install

# 3. Clear cache
npm cache clean --force
```

### Database Issues
```powershell
# Reset everything
rmdir /S /Q chroma_db
curl -X POST http://localhost:8000/documents/reindex
```

---

## 🔍 Useful One-Liners

### Check Everything
```powershell
# All in one
python --version; node --version; ollama list
```

### Quick Health Check
```powershell
# Test all services
curl http://localhost:8000/health; curl http://localhost:3000
```

### Monitor Resources
```powershell
# CPU/Memory usage
Get-Process python, node | Select-Object Name, CPU, WS
```

### Find Large Files
```powershell
# Find files > 100MB
Get-ChildItem -Recurse | Where-Object {$_.Length -gt 100MB} | Select-Object Name, @{N="SizeMB";E={$_.Length / 1MB}}
```

---

## 📊 Monitoring Commands

### System Resources
```powershell
# CPU usage
Get-Counter '\Processor(_Total)\% Processor Time'

# Memory usage
Get-Process python, node | Measure-Object WS -Sum

# Disk space
Get-PSDrive C
```

### API Statistics
```powershell
# Request count (if logging enabled)
Select-String "POST /chat" logs.txt | Measure-Object

# Error count
Select-String "ERROR" logs.txt | Measure-Object
```

---

## 🎨 Customization Commands

### Change Colors (Frontend)
```powershell
# Edit Tailwind config
notepad frontend\tailwind.config.js

# Change primary color theme
```

### Change Model
```powershell
# Edit backend config
notepad backend\.env

# Change OLLAMA_MODEL
# Restart: Ctrl+C then python main.py
```

### Add Sample Data
```powershell
# Copy PDFs
copy C:\Documents\*.pdf data\

# Reindex
curl -X POST http://localhost:8000/documents/reindex
```

---

## 🆘 Emergency Commands

### Kill Everything
```powershell
# Nuclear option
taskkill /F /IM python.exe
taskkill /F /IM node.exe
```

### Clean Everything
```powershell
# Full reset
rmdir /S /Q backend\venv
rmdir /S /Q backend\__pycache__
rmdir /S /Q frontend\node_modules
rmdir /S /Q frontend\dist
rmdir /S /Q chroma_db

# Reinstall
cd backend && python -m venv venv && .\venv\Scripts\Activate.ps1 && pip install -r requirements.txt
cd ..\frontend && npm install
```

### Fresh Start
```powershell
# Start from scratch
git clean -fdx  # WARNING: Deletes everything not in git
# Then follow GETTING_STARTED.md
```

---

## 💡 Pro Tips

### Aliases (Add to PowerShell Profile)
```powershell
# Edit profile
notepad $PROFILE

# Add these:
function Start-Backend { cd D:\ML\Local-RAG\backend; .\venv\Scripts\Activate.ps1; python main.py }
function Start-Frontend { cd D:\ML\Local-RAG\frontend; npm run dev }
function Test-System { cd D:\ML\Local-RAG\backend; python test_system.py }

# Now just type:
# Start-Backend
# Start-Frontend
# Test-System
```

### VS Code Tasks
```json
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Backend",
      "type": "shell",
      "command": "cd backend && .\\venv\\Scripts\\Activate.ps1 && python main.py"
    },
    {
      "label": "Start Frontend",
      "type": "shell",
      "command": "cd frontend && npm run dev"
    }
  ]
}
```

---

## 📚 Quick Reference URLs

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000
- **Ollama**: http://localhost:11434
- **Health Check**: http://localhost:8000/health

---

**Save this file for quick reference!** 🚀

*Press Ctrl+F to search for specific commands*
