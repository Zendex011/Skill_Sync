import os
import json
import hashlib
from typing import Optional, Any

class ParserCache:
    """
    Persistent cache for LLM parsing results to reduce latency and cost.
    Results are stored in a JSON file indexed by a hash of the input text and category.
    """
    
    def __init__(self, cache_file: str = ".cache/llm_results.json"):
        self.cache_file = cache_file
        self.cache_dir = os.path.dirname(self.cache_file)
        self._ensure_cache_dir()
        self.cache = self._load_cache()

    def _ensure_cache_dir(self):
        """Create cache directory if it doesn't exist"""
        if self.cache_dir and not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _load_cache(self) -> dict:
        """Load cache from disk"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save_cache(self):
        """Save cache to disk"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"⚠️ Warning: Failed to save cache to {self.cache_file}: {e}")

    def _generate_key(self, text: str, category: str, context: str = "") -> str:
        """Generate a unique MD5 hash key for the input text, category, and prompt context"""
        clean_text = text.strip()
        composite = f"{category}:{context}:{clean_text}".encode('utf-8')
        return hashlib.md5(composite).hexdigest()

    def get(self, text: str, category: str, context: str = "") -> Optional[dict]:
        """
        Retrieve a cached result if it exists.
        
        Args:
            text: Raw input text that was parsed
            category: Classification (e.g., 'resume')
            context: Optional prompt or version string to invalidate cache on logic changes
        """
        key = self._generate_key(text, category, context)
        return self.cache.get(key)

    def set(self, text: str, category: str, result: Any, context: str = ""):
        """
        Store a result in the cache.
        
        Args:
            text: Raw input text
            category: Classification
            result: Data to cache
            context: Optional prompt or version string
        """
        key = self._generate_key(text, category, context)
        self.cache[key] = result
        self._save_cache()
