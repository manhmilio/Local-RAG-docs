"""
Rate Limiting Module - Giới hạn số request
"""
from fastapi import HTTPException, Request, status
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Tuple
import asyncio


class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, requests_per_minute: int = 60, requests_per_hour: int = 1000):
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        
        # Store: {client_id: [(timestamp, count), ...]}
        self.request_history: Dict[str, list] = defaultdict(list)
        self.lock = asyncio.Lock()
    
    def _clean_old_requests(self, client_id: str, now: datetime):
        """Remove requests older than 1 hour"""
        cutoff = now - timedelta(hours=1)
        self.request_history[client_id] = [
            (ts, count) for ts, count in self.request_history[client_id]
            if ts > cutoff
        ]
    
    def _count_requests(self, client_id: str, now: datetime) -> Tuple[int, int]:
        """Count requests in last minute and hour"""
        one_minute_ago = now - timedelta(minutes=1)
        one_hour_ago = now - timedelta(hours=1)
        
        minute_count = sum(
            count for ts, count in self.request_history[client_id]
            if ts > one_minute_ago
        )
        hour_count = sum(
            count for ts, count in self.request_history[client_id]
            if ts > one_hour_ago
        )
        
        return minute_count, hour_count
    
    async def check_rate_limit(self, client_id: str):
        """
        Check if client has exceeded rate limit
        
        Args:
            client_id: Unique identifier for client (IP, API key, etc.)
            
        Raises:
            HTTPException: If rate limit exceeded
        """
        async with self.lock:
            now = datetime.now()
            
            # Clean old requests
            self._clean_old_requests(client_id, now)
            
            # Count current requests
            minute_count, hour_count = self._count_requests(client_id, now)
            
            # Check limits
            if minute_count >= self.requests_per_minute:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded: {self.requests_per_minute} requests per minute",
                    headers={
                        "Retry-After": "60",
                        "X-RateLimit-Limit": str(self.requests_per_minute),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int((now + timedelta(minutes=1)).timestamp()))
                    }
                )
            
            if hour_count >= self.requests_per_hour:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded: {self.requests_per_hour} requests per hour",
                    headers={
                        "Retry-After": "3600",
                        "X-RateLimit-Limit": str(self.requests_per_hour),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int((now + timedelta(hours=1)).timestamp()))
                    }
                )
            
            # Add current request
            self.request_history[client_id].append((now, 1))


# Global rate limiter instance
rate_limiter = RateLimiter()


async def check_rate_limit(request: Request):
    """
    Dependency for rate limiting
    """
    # Sử dụng IP hoặc API key làm client identifier
    client_id = request.client.host if request.client else "unknown"
    
    # Nếu có API key, dùng API key làm identifier
    api_key = request.headers.get("X-API-Key")
    if api_key:
        client_id = f"key_{api_key[:8]}"
    
    await rate_limiter.check_rate_limit(client_id)
