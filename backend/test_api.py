"""
Test Script - Kiểm tra API endpoints
"""
import requests
import json


BASE_URL = "http://localhost:8001"


def test_root():
    """Test root endpoint"""
    print("\n" + "="*60)
    print("Testing: GET /")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_api_info():
    """Test /api/info endpoint"""
    print("\n" + "="*60)
    print("Testing: GET /api/info")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/info")
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("Testing: GET /health")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_chat(api_key=None):
    """Test chat endpoint"""
    print("\n" + "="*60)
    print("Testing: POST /chat")
    print("="*60)
    
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key
    
    data = {
        "message": "Xin chào, bạn có thể giúp gì cho tôi?",
        "conversation_history": [],
        "use_rag": True
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json=data,
            headers=headers
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {result['response'][:200]}...")
            print(f"Sources: {len(result.get('sources', []))} sources")
        else:
            print(f"Error: {response.json()}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_documents_stats():
    """Test documents stats endpoint"""
    print("\n" + "="*60)
    print("Testing: GET /documents/stats")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/documents/stats")
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "🚀 "*20)
    print("API Testing Suite - Medical Chatbot API")
    print("🚀 "*20)
    print(f"\nBase URL: {BASE_URL}")
    print("\nMake sure backend server is running!")
    print("Start with: cd backend && python main.py")
    
    input("\nPress Enter to start testing...")
    
    results = {
        "Root Endpoint": test_root(),
        "API Info": test_api_info(),
        "Health Check": test_health(),
        "Chat Endpoint": test_chat(),
        "Documents Stats": test_documents_stats()
    }
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASSED" if passed_test else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
    
    print("-"*60)
    print(f"Total: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n🎉 All tests passed! API is working correctly!")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Check the errors above.")


if __name__ == "__main__":
    main()
