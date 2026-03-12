# 🚀 BIS Assistant - AI-Powered Bureau of Indian Standards Chatbot

[![Deploy Backend](https://img.shields.io/badge/Deploy-Backend-blue)](https://render.com/new) [![Deploy Frontend](https://img.shields.io/badge/Deploy-Frontend-orange)](https://vercel.com/new)

**Live Demo**: [Try BIS Assistant](https://bis-chatbot.vercel.app)
**Tech Stack**: Next.js 15 | FastAPI | Groq Llama3.3 | RAG (TF-IDF + Numpy)

## 🎯 Features
- ✅ ISI certification, hallmarking, BIS schemes questions
- ✅ Source-cited answers from bis.gov.in
- ✅ Multi-turn conversation memory
- ✅ Fast local RAG (no external embeddings)
- ✅ Fixed sklearn import & sparse matrix errors

## 🏃 Quick Start (Windows)

### Backend
```
cd backend
venv\Scripts\activate.bat
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

### Frontend
```
cd frontend
npm install
npm run dev
```

## 🔧 Fixed Issues
- [x] **sklearn ModuleNotFoundError** → Numpy cosine similarity replacement
- [x] **Sparse matrix matmul error** → `.toarray()` on query vector
- [x] **Syntax/Pylance errors** → Clean code rewrite
- [x] **Lazy module loading** → Works on /ask

## 🧪 Verify
```
# Test RAG pipeline
cd backend
python test_pipeline.py

# Test API
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d "{\"question\": \"ISI mark\"}"
```

## 📱 Full Stack
Frontend (localhost:3000) → Backend (localhost:8000/ask) → TF-IDF search → Groq LLM → Response + sources

**Ready for production deploy!**

## Environment
```
GROQ_API_KEY=your_key_here
```

## License
MIT
