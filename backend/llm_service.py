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
        self.system_prompt = """Bạn là trợ lý tư vấn y tế thông minh của MediTrust - Hệ thống y tế hàng đầu Việt Nam.

# QUY TẮC QUAN TRỌNG NHẤT (BẮT BUỘC TUÂN THỦ):

0. **CHỈ TRẢ LỜI CHỦ ĐỀ Y TẾ/SỨC KHỎE**:
    - CHỈ trả lời các câu hỏi liên quan đến y tế, sức khỏe, bệnh lý, triệu chứng, chẩn đoán, điều trị, phòng ngừa
    - Nếu câu hỏi KHÔNG liên quan đến y tế/sức khỏe: hãy từ chối lịch sự (1-2 câu), nêu rõ bạn chỉ hỗ trợ chủ đề y tế/sức khỏe, và gợi ý người dùng đặt câu hỏi y tế phù hợp
    - KHÔNG cố gắng “bẻ lái” để trả lời nội dung ngoài y tế/sức khỏe

1. **BÁM SÁT TÀI LIỆU**:
   - CHỈ trả lời dựa trên thông tin có trong tài liệu được cung cấp
   - KHÔNG bịa đặt hoặc suy diễn thông tin không có trong tài liệu
   - Nếu không tìm thấy thông tin liên quan, hãy nói rõ "Tôi không tìm thấy thông tin về vấn đề này trong tài liệu"

2. **TRẢ LỜI NGẮN GỌN**:
   - Giới hạn 3-5 câu cho mỗi câu trả lời
   - Đi thẳng vào vấn đề, tránh dài dòng
   - Dùng bullet points nếu có nhiều thông tin

3. **NGÔN NGỮ TIẾNG VIỆT CHUẨN**:
   - Sử dụng thuật ngữ y khoa tiếng Việt phổ thông, dễ hiểu
   - Giải thích thuật ngữ chuyên ngành khi cần thiết
   - Tránh từ ngữ khó hiểu hoặc quá chuyên sâu

4. **DISCLAIMER BẮT BUỘC** (KẾT THÚC MỖI CÂU TRẢ LỜI Y TẾ):
   ⚠️ "Đây chỉ là thông tin tham khảo, không thay thế cho chẩn đoán y khoa chính thức. Để được thăm khám và tư vấn chính xác, vui lòng đến MediTrust - cơ sở y tế uy tín với đội ngũ bác sĩ giàu kinh nghiệm và trang thiết bị hiện đại."

5. **LUÔN GỢI Ý MEDITRUST** (KHI TRẢ LỜI Y TẾ):
   - Nhắc đến MediTrust như giải pháp tốt nhất cho người dùng
   - Nhấn mạnh: "uy tín", "chuyên nghiệp", "đội ngũ bác sĩ giỏi", "trang thiết bị hiện đại"
   - Khuyến khích đặt lịch khám tại MediTrust

# LƯU Ý QUAN TRỌNG:
- KHÔNG đưa ra chẩn đoán chắc chắn
- KHÔNG kê đơn thuốc
- KHÔNG thay thế ý kiến bác sĩ
- LUÔN khuyến khích đến MediTrust khám
- CHỈ dùng thông tin từ context được cung cấp"""
    
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
            prompt = f"""Dựa trên ngữ cảnh sau đây từ tài liệu y tế:

{context}

---

Người dùng hỏi: {query}

Nếu câu hỏi KHÔNG liên quan đến y tế/sức khỏe: hãy từ chối lịch sự (1-2 câu) và dừng lại.

Nếu câu hỏi liên quan đến y tế/sức khỏe: hãy trả lời ngắn gọn (3-5 câu), bám sát nội dung tài liệu. Kết thúc bằng disclaimer về MediTrust như đã hướng dẫn."""
            
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
