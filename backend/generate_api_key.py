"""
Script để tạo API keys cho authentication
"""
import secrets
import sys


def generate_api_key() -> str:
    """Generate a secure random API key"""
    return secrets.token_urlsafe(32)


def main():
    """Generate multiple API keys"""
    print("=" * 60)
    print("API Key Generator for Medical Chatbot API")
    print("=" * 60)
    print()
    
    # Hỏi số lượng keys cần tạo
    try:
        count = int(input("Số lượng API keys cần tạo (mặc định: 1): ") or "1")
    except ValueError:
        count = 1
    
    print()
    print(f"Đang tạo {count} API key(s)...")
    print("-" * 60)
    
    keys = []
    for i in range(count):
        key = generate_api_key()
        keys.append(key)
        print(f"{i+1}. {key}")
    
    print("-" * 60)
    print()
    print("Để sử dụng các API keys này:")
    print("1. Copy các keys trên")
    print("2. Thêm vào file .env trong thư mục backend/:")
    print()
    print("   ENABLE_API_KEY_AUTH=true")
    print(f"   API_KEYS={','.join(keys)}")
    print()
    print("3. Restart backend server")
    print()
    print("Khi gọi API, thêm header:")
    print('   X-API-Key: <your-api-key>')
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
