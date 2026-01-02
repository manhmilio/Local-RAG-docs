#!/usr/bin/env python3
"""
Script để test các components của hệ thống
"""
import sys
import asyncio
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from vector_store import VectorStore
from llm_service import LLMService
from pdf_processor import PDFProcessor


async def test_vector_store():
    """Test ChromaDB và embeddings"""
    print("\n🧪 Testing VectorStore...")
    
    try:
        vs = VectorStore()
        
        # Test embedding
        texts = ["Bệnh cảm cúm", "Triệu chứng sốt"]
        embeddings = vs.embed_texts(texts)
        print(f"✅ Embeddings: {len(embeddings)} vectors")
        
        # Test add documents
        count = vs.add_documents(
            texts=texts,
            metadatas=[{"source": "test1"}, {"source": "test2"}]
        )
        print(f"✅ Added {count} documents")
        
        # Test search
        docs, metas, scores = vs.similarity_search("triệu chứng", top_k=2)
        print(f"✅ Search results: {len(docs)} documents")
        
        return True
    except Exception as e:
        print(f"❌ VectorStore test failed: {str(e)}")
        return False


async def test_llm_service():
    """Test Ollama connection"""
    print("\n🧪 Testing LLM Service...")
    
    try:
        vs = VectorStore()
        llm = LLMService(vs)
        
        # Test connection
        is_connected = llm.check_ollama_connection()
        print(f"{'✅' if is_connected else '❌'} Ollama connection: {is_connected}")
        
        # Test list models
        models = llm.list_available_models()
        print(f"✅ Available models: {models}")
        
        return is_connected
    except Exception as e:
        print(f"❌ LLM Service test failed: {str(e)}")
        return False


async def test_pdf_processor():
    """Test PDF processing"""
    print("\n🧪 Testing PDF Processor...")
    
    try:
        vs = VectorStore()
        processor = PDFProcessor(vs)
        
        # Test text cleaning
        text = "  Multiple   spaces   here  "
        cleaned = processor.clean_text(text)
        print(f"✅ Text cleaning works: '{cleaned}'")
        
        # Test chunking
        long_text = "Lorem ipsum. " * 100
        chunks = processor.chunk_text(long_text, {"source": "test"})
        print(f"✅ Created {len(chunks)} chunks")
        
        return True
    except Exception as e:
        print(f"❌ PDF Processor test failed: {str(e)}")
        return False


async def test_end_to_end():
    """Test full RAG pipeline"""
    print("\n🧪 Testing End-to-End RAG Pipeline...")
    
    try:
        # Setup
        vs = VectorStore()
        llm = LLMService(vs)
        
        # Add test documents
        docs = [
            "Bệnh cảm cúm là bệnh nhiễm trùng đường hô hấp do virus cúm gây ra. Các triệu chứng bao gồm sốt, ho, đau họng.",
            "Triệu chứng thường gặp của cảm cúm: sốt cao, đau đầu, mệt mỏi, ho khô, đau cơ.",
            "Để phòng ngừa cảm cúm, nên tiêm vaccine hàng năm và rửa tay thường xuyên."
        ]
        
        vs.add_documents(
            texts=docs,
            metadatas=[{"source": f"test_doc_{i}"} for i in range(len(docs))]
        )
        print("✅ Added test documents")
        
        # Test query
        response, sources = await llm.generate_response(
            query="Triệu chứng của cảm cúm là gì?",
            use_rag=True
        )
        
        print(f"✅ Generated response: {len(response)} characters")
        print(f"✅ Sources: {sources}")
        print(f"\n📝 Response preview:\n{response[:200]}...")
        
        return True
    except Exception as e:
        print(f"❌ End-to-end test failed: {str(e)}")
        return False


async def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 Medical Chatbot - System Tests")
    print("=" * 60)
    
    print(f"\n⚙️  Configuration:")
    print(f"   - Ollama Model: {settings.OLLAMA_MODEL}")
    print(f"   - Ollama URL: {settings.OLLAMA_BASE_URL}")
    print(f"   - Embedding Model: {settings.EMBEDDING_MODEL}")
    print(f"   - ChromaDB: {settings.CHROMA_PERSIST_DIRECTORY}")
    
    results = {}
    
    # Run tests
    results["VectorStore"] = await test_vector_store()
    results["LLM Service"] = await test_llm_service()
    results["PDF Processor"] = await test_pdf_processor()
    
    if all([results["VectorStore"], results["LLM Service"]]):
        results["End-to-End"] = await test_end_to_end()
    else:
        print("\n⚠️  Skipping end-to-end test due to previous failures")
        results["End-to-End"] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    all_passed = all(results.values())
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check output above.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
