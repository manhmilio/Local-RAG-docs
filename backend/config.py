"""
Configuration Module - Quản lý các biến môi trường và cấu hình hệ thống
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Cấu hình hệ thống từ environment variables"""
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "mistral:7b"
    
    # ChromaDB Configuration
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "medical_documents"
    
    # Embedding Model
    EMBEDDING_MODEL: str = "paraphrase-multilingual-MiniLM-L12-v2"
    
    # PDF Data Path
    PDF_DATA_PATH: str = "./data"
    
    # LLM Parameters
    TEMPERATURE: float = 0.3
    MAX_TOKENS: int = 2048
    TOP_P: float = 0.9
    
    # Retrieval Configuration
    TOP_K_RESULTS: int = 3
    SIMILARITY_THRESHOLD: float = 0.7
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins thành list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton instance
settings = Settings()
