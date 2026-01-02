"""
Main FastAPI Application - Entry point của backend
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator, Optional
import json

from config import settings
from models import (
    ChatRequest, 
    ChatResponse, 
    HealthResponse,
    DocumentUploadResponse,
    EmbeddingStats
)
from vector_store import VectorStore
from llm_service import LLMService
from pdf_processor import PDFProcessor
from auth import verify_api_key, optional_verify_api_key
from rate_limiter import check_rate_limit, rate_limiter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global instances
vector_store: VectorStore = None
llm_service: LLMService = None
pdf_processor: PDFProcessor = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management - khởi tạo và cleanup resources"""
    global vector_store, llm_service, pdf_processor
    
    logger.info("🚀 Khởi động ứng dụng Medical Chatbot...")
    
    try:
        # Khởi tạo Vector Store
        logger.info("Đang khởi tạo ChromaDB Vector Store...")
        vector_store = VectorStore()
        
        # Khởi tạo LLM Service
        logger.info(f"Đang kết nối Ollama với model: {settings.OLLAMA_MODEL}...")
        llm_service = LLMService(vector_store)
        
        # Khởi tạo PDF Processor
        logger.info("Đang khởi tạo PDF Processor...")
        pdf_processor = PDFProcessor(vector_store)
        
        logger.info("✅ Khởi động thành công!")
        
    except Exception as e:
        logger.error(f"❌ Lỗi khi khởi động: {str(e)}")
        raise
    
    yield
    
    # Cleanup
    logger.info("🛑 Đang dừng ứng dụng...")


# Khởi tạo FastAPI app
app = FastAPI(
    title="Medical Chatbot API",
    description="API cho hệ thống chatbot chẩn đoán bệnh với RAG. Hỗ trợ kết nối từ bất kỳ dự án nào thông qua REST API.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset"]
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Medical Chatbot API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "chat": "/chat",
            "chat_stream": "/chat/stream",
            "upload": "/documents/upload",
            "stats": "/documents/stats"
        },
        "authentication": settings.ENABLE_API_KEY_AUTH,
        "rate_limiting": settings.ENABLE_RATE_LIMITING
    }


@app.get("/api/info", tags=["Root"])
async def api_info():
    """
    Lấy thông tin chi tiết về API và cấu hình hệ thống
    """
    return {
        "api_version": "1.0.0",
        "model": settings.OLLAMA_MODEL,
        "embedding_model": settings.EMBEDDING_MODEL,
        "features": {
            "rag_enabled": True,
            "streaming_support": True,
            "document_upload": True,
            "multilingual": True
        },
        "limits": {
            "max_tokens": settings.MAX_TOKENS,
            "rate_limit_per_minute": settings.RATE_LIMIT_PER_MINUTE if settings.ENABLE_RATE_LIMITING else None,
            "rate_limit_per_hour": settings.RATE_LIMIT_PER_HOUR if settings.ENABLE_RATE_LIMITING else None
        },
        "authentication": {
            "required": settings.ENABLE_API_KEY_AUTH,
            "method": "API Key (Header: X-API-Key)" if settings.ENABLE_API_KEY_AUTH else "None"
        },
        "cors": {
            "allow_all_origins": settings.ALLOW_ALL_ORIGINS,
            "allowed_origins": settings.cors_origins_list if not settings.ALLOW_ALL_ORIGINS else ["*"]
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint - kiểm tra trạng thái hệ thống
    """
    try:
        ollama_status = llm_service.check_ollama_connection()
        chroma_status = vector_store is not None
        
        return HealthResponse(
            status="healthy" if (ollama_status and chroma_status) else "degraded",
            ollama_connected=ollama_status,
            chroma_initialized=chroma_status
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail=str(e))


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(
    request: ChatRequest,
    req: Request,
    api_key: str = Depends(optional_verify_api_key)
):
    """
    Chat endpoint - xử lý câu hỏi từ người dùng
    
    Args:
        request: ChatRequest chứa message và lịch sử hội thoại
        
    Returns:
        ChatResponse với câu trả lời và sources
        
    Headers:
        X-API-Key: API key for authentication (if enabled)
    """
    # Check rate limit
    if settings.ENABLE_RATE_LIMITING:
        await check_rate_limit(req)
    
    try:
        logger.info(f"Nhận câu hỏi: {request.message[:100]}...")
        
        # Gọi LLM service để xử lý
        response, sources = await llm_service.generate_response(
            query=request.message,
            conversation_history=request.conversation_history,
            use_rag=request.use_rag
        )
        
        return ChatResponse(
            response=response,
            sources=sources if request.use_rag else []
        )
        
    except Exception as e:
        logger.error(f"Lỗi khi xử lý chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý: {str(e)}")


@app.post("/chat/stream", tags=["Chat"])
async def chat_stream(
    request: ChatRequest,
    req: Request,
    api_key: str = Depends(optional_verify_api_key)
):
    """
    Streaming chat endpoint - trả về response theo real-time
    
    Returns:
        StreamingResponse với Server-Sent Events (SSE)
        
    Headers:
        X-API-Key: API key for authentication (if enabled)
    """
    # Check rate limit
    if settings.ENABLE_RATE_LIMITING:
        await check_rate_limit(req)
    
    async def generate_stream() -> AsyncGenerator[str, None]:
        try:
            async for chunk in llm_service.stream_response(
                query=request.message,
                conversation_history=request.conversation_history,
                use_rag=request.use_rag
            ):
                # Format as SSE
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                
        except Exception as e:
            logger.error(f"Lỗi streaming: {str(e)}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@app.post("/documents/upload", response_model=DocumentUploadResponse, tags=["Documents"])
async def upload_document(
    file: UploadFile = File(...),
    api_key: str = Depends(verify_api_key)
):
    """
    Upload và xử lý tài liệu PDF y tế
    
    Args:
        file: PDF file upload
        
    Returns:
        DocumentUploadResponse với thông tin xử lý
        
    Headers:
        X-API-Key: API key for authentication (required if auth is enabled)
    """
    try:
        # Kiểm tra file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Chỉ chấp nhận file PDF"
            )
        
        logger.info(f"Đang xử lý file: {file.filename}")
        
        # Đọc file content
        content = await file.read()
        
        # Process PDF
        chunks_created = await pdf_processor.process_pdf(
            content=content,
            filename=file.filename
        )
        
        return DocumentUploadResponse(
            filename=file.filename,
            chunks_created=chunks_created,
            status="success",
            message=f"Đã xử lý thành công {chunks_created} chunks từ {file.filename}"
        )
        
    except Exception as e:
        logger.error(f"Lỗi khi upload document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents/stats", response_model=EmbeddingStats, tags=["Documents"])
async def get_document_stats():
    """
    Lấy thống kê về tài liệu trong vector store
    """
    try:
        stats = vector_store.get_stats()
        return EmbeddingStats(**stats)
    except Exception as e:
        logger.error(f"Lỗi khi lấy stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/documents/reindex", tags=["Documents"])
async def reindex_documents(api_key: str = Depends(verify_api_key)):
    """
    Reindex tất cả PDF files trong thư mục data
    
    Headers:
        X-API-Key: API key for authentication (required if auth is enabled)
    """
    try:
        logger.info("Bắt đầu reindex documents...")
        result = await pdf_processor.reindex_all_pdfs()
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Lỗi khi reindex: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )
