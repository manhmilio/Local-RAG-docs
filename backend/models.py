"""
Data Models - Định nghĩa các Pydantic models cho API
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ChatMessage(BaseModel):
    """Model cho một tin nhắn chat"""
    role: str = Field(..., description="Vai trò: 'user' hoặc 'assistant'")
    content: str = Field(..., description="Nội dung tin nhắn")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)


class ChatRequest(BaseModel):
    """Request body cho chat endpoint"""
    message: str = Field(..., min_length=1, description="Câu hỏi từ người dùng")
    conversation_history: Optional[List[ChatMessage]] = Field(
        default=[],
        description="Lịch sử hội thoại (optional)"
    )
    use_rag: bool = Field(
        default=True,
        description="Có sử dụng RAG (Retrieval Augmented Generation) không"
    )


class ChatResponse(BaseModel):
    """Response cho chat endpoint"""
    response: str = Field(..., description="Câu trả lời từ chatbot")
    sources: Optional[List[str]] = Field(
        default=[],
        description="Các nguồn tài liệu được tham khảo"
    )
    timestamp: datetime = Field(default_factory=datetime.now)


class DocumentUploadResponse(BaseModel):
    """Response khi upload tài liệu PDF"""
    filename: str
    chunks_created: int
    status: str
    message: str


class HealthResponse(BaseModel):
    """Response cho health check endpoint"""
    status: str
    ollama_connected: bool
    chroma_initialized: bool
    timestamp: datetime = Field(default_factory=datetime.now)


class EmbeddingStats(BaseModel):
    """Thống kê về embeddings trong database"""
    total_documents: int
    total_chunks: int
    collection_name: str
