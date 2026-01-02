"""
Vector Store Module - Quản lý ChromaDB và embeddings
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional, Tuple
import logging
from config import settings

logger = logging.getLogger(__name__)


class VectorStore:
    """
    Class quản lý ChromaDB vector store và embeddings
    """
    
    def __init__(self):
        """Khởi tạo ChromaDB client và embedding model"""
        try:
            # Khởi tạo embedding model
            logger.info(f"Đang load embedding model: {settings.EMBEDDING_MODEL}")
            self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
            
            # Khởi tạo ChromaDB client với persistent storage
            logger.info(f"Đang kết nối ChromaDB: {settings.CHROMA_PERSIST_DIRECTORY}")
            self.client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIRECTORY,
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Lấy hoặc tạo collection
            self.collection = self.client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}  # Sử dụng cosine similarity
            )
            
            logger.info(f"✅ ChromaDB initialized - Collection: {settings.CHROMA_COLLECTION_NAME}")
            
        except Exception as e:
            logger.error(f"❌ Lỗi khởi tạo VectorStore: {str(e)}")
            raise
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Tạo embeddings cho list of texts
        
        Args:
            texts: Danh sách các đoạn text cần embed
            
        Returns:
            List of embeddings (vectors)
        """
        try:
            embeddings = self.embedding_model.encode(
                texts,
                convert_to_numpy=True,
                show_progress_bar=False
            )
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Lỗi khi tạo embeddings: {str(e)}")
            raise
    
    def add_documents(
        self,
        texts: List[str],
        metadatas: List[Dict],
        ids: Optional[List[str]] = None
    ) -> int:
        """
        Thêm documents vào vector store
        
        Args:
            texts: Danh sách text chunks
            metadatas: Metadata cho mỗi chunk
            ids: IDs cho mỗi chunk (tự động generate nếu không có)
            
        Returns:
            Số lượng documents đã thêm
        """
        try:
            if not texts:
                return 0
            
            # Generate IDs nếu không có
            if ids is None:
                import uuid
                ids = [str(uuid.uuid4()) for _ in range(len(texts))]
            
            # Tạo embeddings
            logger.info(f"Đang tạo embeddings cho {len(texts)} chunks...")
            embeddings = self.embed_texts(texts)
            
            # Thêm vào ChromaDB
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"✅ Đã thêm {len(texts)} documents vào vector store")
            return len(texts)
            
        except Exception as e:
            logger.error(f"Lỗi khi thêm documents: {str(e)}")
            raise
    
    def similarity_search(
        self,
        query: str,
        top_k: int = None,
        filter_metadata: Optional[Dict] = None
    ) -> Tuple[List[str], List[Dict], List[float]]:
        """
        Tìm kiếm semantic similarity
        
        Args:
            query: Câu query cần tìm
            top_k: Số lượng kết quả trả về
            filter_metadata: Filter theo metadata
            
        Returns:
            Tuple of (documents, metadatas, distances)
        """
        try:
            if top_k is None:
                top_k = settings.TOP_K_RESULTS
            
            # Tạo embedding cho query
            query_embedding = self.embed_texts([query])[0]
            
            # Query ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=filter_metadata
            )
            
            # Parse results
            documents = results['documents'][0] if results['documents'] else []
            metadatas = results['metadatas'][0] if results['metadatas'] else []
            distances = results['distances'][0] if results['distances'] else []
            
            # Filter theo similarity threshold
            filtered_results = []
            for doc, meta, dist in zip(documents, metadatas, distances):
                # ChromaDB trả về distance (càng nhỏ càng giống)
                # Convert sang similarity score (1 - distance)
                similarity = 1 - dist
                if similarity >= settings.SIMILARITY_THRESHOLD:
                    filtered_results.append((doc, meta, similarity))
            
            if filtered_results:
                docs, metas, sims = zip(*filtered_results)
                logger.info(f"Tìm thấy {len(docs)} relevant documents")
                return list(docs), list(metas), list(sims)
            else:
                logger.info("Không tìm thấy documents phù hợp")
                return [], [], []
                
        except Exception as e:
            logger.error(f"Lỗi khi search: {str(e)}")
            return [], [], []
    
    def get_stats(self) -> Dict:
        """
        Lấy thống kê về collection
        
        Returns:
            Dictionary chứa stats
        """
        try:
            count = self.collection.count()
            
            return {
                "total_documents": count,
                "total_chunks": count,  # Mỗi document là 1 chunk
                "collection_name": settings.CHROMA_COLLECTION_NAME
            }
        except Exception as e:
            logger.error(f"Lỗi khi lấy stats: {str(e)}")
            return {
                "total_documents": 0,
                "total_chunks": 0,
                "collection_name": settings.CHROMA_COLLECTION_NAME
            }
    
    def delete_collection(self):
        """Xóa collection (dùng cho reset/reindex)"""
        try:
            self.client.delete_collection(settings.CHROMA_COLLECTION_NAME)
            logger.info(f"Đã xóa collection: {settings.CHROMA_COLLECTION_NAME}")
            
            # Tạo lại collection
            self.collection = self.client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            logger.error(f"Lỗi khi xóa collection: {str(e)}")
            raise
    
    def check_connection(self) -> bool:
        """Kiểm tra connection với ChromaDB"""
        try:
            self.collection.count()
            return True
        except:
            return False
