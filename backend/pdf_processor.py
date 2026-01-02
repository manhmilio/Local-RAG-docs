"""
PDF Processor Module - Xử lý và chunk tài liệu PDF y tế
"""
from PyPDF2 import PdfReader
from typing import List, Dict, Tuple
import logging
import io
import os
from pathlib import Path
import re
import hashlib

from config import settings
from vector_store import VectorStore

logger = logging.getLogger(__name__)


class PDFProcessor:
    """
    Class xử lý PDF documents - đọc, chunk, và embed vào vector store
    """
    
    def __init__(self, vector_store: VectorStore):
        """
        Args:
            vector_store: Instance của VectorStore để lưu embeddings
        """
        self.vector_store = vector_store
        self.chunk_size = 1000  # Số ký tự mỗi chunk
        self.chunk_overlap = 200  # Overlap giữa các chunks
    
    def extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """
        Trích xuất text từ PDF file
        
        Args:
            pdf_content: Binary content của PDF file
            
        Returns:
            Text đã extract
        """
        try:
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PdfReader(pdf_file)
            
            text_parts = []
            for page_num, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                if text.strip():
                    text_parts.append(f"[Page {page_num + 1}]\n{text}")
            
            full_text = "\n\n".join(text_parts)
            logger.info(f"Extracted {len(full_text)} characters from PDF")
            
            return full_text
            
        except Exception as e:
            logger.error(f"Lỗi khi extract text từ PDF: {str(e)}")
            raise
    
    def clean_text(self, text: str) -> str:
        """
        Làm sạch text - xóa ký tự đặc biệt, normalize whitespace
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Xóa multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Xóa special characters nhưng giữ tiếng Việt
        text = re.sub(r'[^\w\s\u00C0-\u1EF9.,;:!?()-]', '', text)
        
        # Normalize newlines
        text = text.replace('\n', ' ')
        
        return text.strip()
    
    def chunk_text(self, text: str, metadata: Dict) -> List[Tuple[str, Dict]]:
        """
        Chia text thành các chunks nhỏ với overlap
        
        Args:
            text: Text cần chunk
            metadata: Metadata cơ bản cho document
            
        Returns:
            List of (chunk_text, chunk_metadata)
        """
        chunks = []
        
        # Clean text trước
        text = self.clean_text(text)
        
        # Chia thành các chunks
        start = 0
        chunk_id = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Tìm điểm ngắt tự nhiên (. hoặc \n) gần end
            if end < len(text):
                # Tìm dấu chấm gần nhất
                period_pos = text.rfind('.', start, end)
                if period_pos > start + self.chunk_size * 0.5:  # Không quá ngắn
                    end = period_pos + 1
            
            chunk = text[start:end].strip()
            
            if chunk:
                chunk_metadata = {
                    **metadata,
                    "chunk_id": chunk_id,
                    "start_char": start,
                    "end_char": end
                }
                chunks.append((chunk, chunk_metadata))
                chunk_id += 1
            
            # Move start với overlap
            start = end - self.chunk_overlap
        
        logger.info(f"Created {len(chunks)} chunks from document")
        return chunks
    
    async def process_pdf(self, content: bytes, filename: str) -> int:
        """
        Xử lý PDF file - extract, chunk, và embed vào vector store
        
        Args:
            content: Binary content của PDF
            filename: Tên file
            
        Returns:
            Số chunks đã tạo
        """
        try:
            logger.info(f"Processing PDF: {filename}")
            
            # Extract text
            text = self.extract_text_from_pdf(content)
            
            if not text.strip():
                raise ValueError("Không extract được text từ PDF")
            
            # Tạo metadata cho document
            doc_id = hashlib.md5(filename.encode()).hexdigest()
            base_metadata = {
                "source": filename,
                "document_id": doc_id,
                "type": "medical_document"
            }
            
            # Chunk text
            chunks = self.chunk_text(text, base_metadata)
            
            # Chuẩn bị dữ liệu cho vector store
            texts = [chunk[0] for chunk in chunks]
            metadatas = [chunk[1] for chunk in chunks]
            ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
            
            # Thêm vào vector store
            count = self.vector_store.add_documents(
                texts=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            return count
            
        except Exception as e:
            logger.error(f"Lỗi khi process PDF {filename}: {str(e)}")
            raise
    
    async def reindex_all_pdfs(self) -> Dict:
        """
        Reindex tất cả PDF files trong thư mục data
        
        Returns:
            Dictionary với kết quả
        """
        try:
            data_path = Path(settings.PDF_DATA_PATH)
            
            if not data_path.exists():
                os.makedirs(data_path, exist_ok=True)
                return {
                    "status": "success",
                    "message": "Data folder created but empty",
                    "files_processed": 0
                }
            
            # Tìm tất cả PDF files
            pdf_files = list(data_path.glob("*.pdf"))
            
            if not pdf_files:
                return {
                    "status": "success",
                    "message": "No PDF files found",
                    "files_processed": 0
                }
            
            logger.info(f"Found {len(pdf_files)} PDF files to process")
            
            # Reset collection
            self.vector_store.delete_collection()
            
            # Process từng file
            total_chunks = 0
            processed_files = []
            
            for pdf_path in pdf_files:
                try:
                    with open(pdf_path, 'rb') as f:
                        content = f.read()
                    
                    chunks = await self.process_pdf(content, pdf_path.name)
                    total_chunks += chunks
                    processed_files.append({
                        "filename": pdf_path.name,
                        "chunks": chunks
                    })
                    
                except Exception as e:
                    logger.error(f"Lỗi khi process {pdf_path.name}: {str(e)}")
                    processed_files.append({
                        "filename": pdf_path.name,
                        "error": str(e)
                    })
            
            return {
                "status": "success",
                "message": f"Processed {len(processed_files)} files",
                "total_chunks": total_chunks,
                "files": processed_files
            }
            
        except Exception as e:
            logger.error(f"Lỗi khi reindex: {str(e)}")
            raise
    
    def extract_medical_entities(self, text: str) -> List[str]:
        """
        Extract các entities y tế từ text (optional enhancement)
        
        Args:
            text: Text cần extract
            
        Returns:
            List of medical entities
        """
        # TODO: Implement NER cho y tế nếu cần
        # Có thể dùng spaCy với medical NER model
        return []
