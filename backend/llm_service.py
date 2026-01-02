"""
LLM Service Module - Tích hợp Ollama với LangChain và RAG pipeline
"""
import ollama
from typing import List, Optional, Tuple, AsyncGenerator
import logging
from config import settings
from models import ChatMessage
from vector_store import VectorStore

logger = logging.getLogger(__name__)


class LLMService:
    """
    Service xử lý LLM requests với Ollama và RAG
    """
    
    def __init__(self, vector_store: VectorStore):
        """
        Args:
            vector_store: Instance của VectorStore để retrieve context
        """
        self.vector_store = vector_store
        self.model = settings.OLLAMA_MODEL
        self.client = ollama.Client(host=settings.OLLAMA_BASE_URL)
        
        # System prompt cho medical chatbot
        self.system_prompt = """Bạn là một trợ lý y tế AI thông minh và chuyên nghiệp. 
Nhiệm vụ của bạn là:
1. Trả lời các câu hỏi về triệu chứng và bệnh tật dựa trên thông tin y tế được cung cấp
2. Giải thích rõ ràng, dễ hiểu bằng tiếng Việt
3. Luôn khuyên người dùng nên gặp bác sĩ để chẩn đoán chính xác
4. KHÔNG tự ý chẩn đoán hoặc kê đơn thuốc
5. Nếu không chắc chắn, hãy thừa nhận và đề nghị tìm kiếm ý kiến chuyên gia

Hãy trả lời một cách thân thiện, có cấu trúc, và chuyên nghiệp."""
    
    def check_ollama_connection(self) -> bool:
        """
        Kiểm tra connection với Ollama server
        
        Returns:
            True nếu kết nối thành công
        """
        try:
            # List models để test connection
            self.client.list()
            logger.info("✅ Ollama connection OK")
            return True
        except Exception as e:
            logger.error(f"❌ Ollama connection failed: {str(e)}")
            return False
    
    def build_context_prompt(self, query: str, use_rag: bool = True) -> Tuple[str, List[str]]:
        """
        Build prompt với context từ RAG
        
        Args:
            query: Câu hỏi từ user
            use_rag: Có sử dụng RAG không
            
        Returns:
            Tuple of (prompt, sources)
        """
        sources = []
        
        if not use_rag:
            return query, sources
        
        try:
            # Retrieve relevant documents
            docs, metadatas, scores = self.vector_store.similarity_search(
                query=query,
                top_k=settings.TOP_K_RESULTS
            )
            
            if not docs:
                logger.info("Không tìm thấy context từ documents")
                return query, sources
            
            # Build context
            context_parts = []
            for i, (doc, meta, score) in enumerate(zip(docs, metadatas, scores), 1):
                context_parts.append(f"[Tài liệu {i}] (Độ liên quan: {score:.2f})\n{doc}")
                sources.append(meta.get('source', 'Unknown'))
            
            context = "\n\n".join(context_parts)
            
            # Build full prompt
            prompt = f"""Dựa trên các thông tin y tế sau:

{context}

---

Câu hỏi: {query}

Hãy trả lời câu hỏi dựa trên thông tin được cung cấp ở trên. Nếu thông tin không đủ để trả lời, hãy nói rõ điều đó."""
            
            logger.info(f"Built RAG prompt with {len(docs)} documents")
            return prompt, sources
            
        except Exception as e:
            logger.error(f"Lỗi khi build context: {str(e)}")
            return query, sources
    
    def build_conversation_messages(
        self,
        query: str,
        conversation_history: Optional[List[ChatMessage]] = None
    ) -> List[dict]:
        """
        Build messages list cho Ollama từ conversation history
        
        Args:
            query: Current query
            conversation_history: Previous messages
            
        Returns:
            List of message dicts
        """
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Add conversation history
        if conversation_history:
            for msg in conversation_history[-10:]:  # Lấy 10 messages gần nhất
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # Add current query
        messages.append({
            "role": "user",
            "content": query
        })
        
        return messages
    
    async def generate_response(
        self,
        query: str,
        conversation_history: Optional[List[ChatMessage]] = None,
        use_rag: bool = True
    ) -> Tuple[str, List[str]]:
        """
        Generate response từ LLM (non-streaming)
        
        Args:
            query: User query
            conversation_history: Previous messages
            use_rag: Có sử dụng RAG không
            
        Returns:
            Tuple of (response, sources)
        """
        try:
            # Build prompt với RAG context
            enhanced_query, sources = self.build_context_prompt(query, use_rag)
            
            # Build messages
            messages = self.build_conversation_messages(
                enhanced_query,
                conversation_history
            )
            
            logger.info(f"Generating response với model: {self.model}")
            
            # Call Ollama
            response = self.client.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": settings.TEMPERATURE,
                    "num_predict": settings.MAX_TOKENS,
                    "top_p": settings.TOP_P
                }
            )
            
            answer = response['message']['content']
            logger.info(f"Generated response: {len(answer)} characters")
            
            return answer, sources
            
        except Exception as e:
            logger.error(f"Lỗi khi generate response: {str(e)}")
            raise
    
    async def stream_response(
        self,
        query: str,
        conversation_history: Optional[List[ChatMessage]] = None,
        use_rag: bool = True
    ) -> AsyncGenerator[str, None]:
        """
        Stream response từ LLM real-time
        
        Args:
            query: User query
            conversation_history: Previous messages
            use_rag: Có sử dụng RAG không
            
        Yields:
            Chunks of response text
        """
        try:
            # Build prompt với RAG context
            enhanced_query, sources = self.build_context_prompt(query, use_rag)
            
            # Build messages
            messages = self.build_conversation_messages(
                enhanced_query,
                conversation_history
            )
            
            logger.info(f"Streaming response với model: {self.model}")
            
            # Stream từ Ollama
            stream = self.client.chat(
                model=self.model,
                messages=messages,
                stream=True,
                options={
                    "temperature": settings.TEMPERATURE,
                    "num_predict": settings.MAX_TOKENS,
                    "top_p": settings.TOP_P
                }
            )
            
            # Yield sources trước (nếu có)
            if sources and use_rag:
                sources_text = "\n\n**📚 Nguồn tham khảo:**\n" + "\n".join(
                    f"- {src}" for src in set(sources)
                )
                yield sources_text + "\n\n---\n\n"
            
            # Yield từng chunk
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    content = chunk['message']['content']
                    yield content
            
            logger.info("Streaming completed")
            
        except Exception as e:
            logger.error(f"Lỗi khi stream response: {str(e)}")
            yield f"\n\n❌ Lỗi: {str(e)}"
    
    def pull_model(self, model_name: Optional[str] = None):
        """
        Pull/download model từ Ollama registry
        
        Args:
            model_name: Tên model (default: settings.OLLAMA_MODEL)
        """
        try:
            model = model_name or self.model
            logger.info(f"Pulling model: {model}")
            
            self.client.pull(model)
            logger.info(f"✅ Model {model} pulled successfully")
            
        except Exception as e:
            logger.error(f"Lỗi khi pull model: {str(e)}")
            raise
    
    def list_available_models(self) -> List[str]:
        """
        List các models có sẵn trong Ollama
        
        Returns:
            List of model names
        """
        try:
            models = self.client.list()
            return [model['name'] for model in models.get('models', [])]
        except Exception as e:
            logger.error(f"Lỗi khi list models: {str(e)}")
            return []
