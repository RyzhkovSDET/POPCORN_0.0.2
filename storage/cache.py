"""
Cache module for storing and managing API responses with TTL (Time To Live).
"""
import time
import json
from typing import Any, Optional


class CacheManager:
    """Manages in-memory cache with TTL support."""
    
    def __init__(self):
        """Initialize cache storage."""
        self._cache = {}
    
    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """
        Store a value in cache with optional TTL.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (default: 300)
        """
        self._cache[key] = {
            'value': value,
            'timestamp': time.time(),
            'ttl': ttl
        }
    
    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from cache if not expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if expired/not found
        """
        if key not in self._cache:
            return None
        
        cached_item = self._cache[key]
        elapsed = time.time() - cached_item['timestamp']
        
        if elapsed > cached_item['ttl']:
            del self._cache[key]
            return None
        
        return cached_item['value']
    
    def clear(self) -> None:
        """Clear all cached items."""
        self._cache.clear()
    
    def get_cache_info(self) -> dict:
        """Get cache statistics."""
        return {
            'items': len(self._cache),
            'keys': list(self._cache.keys())
        }


# Global cache instance
_cache_manager = CacheManager()


def get_cache_manager() -> CacheManager:
    """Get the global cache manager instance."""
    return _cache_manager
