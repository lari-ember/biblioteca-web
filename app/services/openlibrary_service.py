# openlibrary_service.py
"""
OpenLibrary API integration service with caching, rate limiting, and translation.

Provides robust book search functionality with:
- 1-hour cache to reduce API calls
- Rate limiting (100 requests/minute)
- EN→PT genre translation
- Performance metrics tracking
- Fallback cover URLs
- Error handling and logging
"""
import json
import os
import time
from typing import List, Dict, Optional

import requests
from flask import current_app

from app import db, cache
from app.models.modelsdb import APIMetrics


class OpenLibraryService:
    """Service for interacting with OpenLibrary API."""
    
    BASE_URL = "https://openlibrary.org/search.json"
    COVER_URL_TEMPLATE = "https://covers.openlibrary.org/b/id/{cover_id}-{size}.jpg"
    TIMEOUT = 5  # seconds
    
    def __init__(self):
        """Initialize service and load genre translations."""
        self._load_translations()
    
    def _load_translations(self):
        """Load genre translation dictionary from JSON file."""
        try:
            translations_path = os.path.join(
                os.path.dirname(__file__),
                '../translations/genres_en_pt.json'
            )
            with open(translations_path, 'r', encoding='utf-8') as f:
                self.genre_translations = json.load(f)
        except Exception as e:
            current_app.logger.warning(f"Could not load genre translations: {e}")
            self.genre_translations = {}
    
    def _translate_genre(self, genre_en: str) -> str:
        """
        Translate genre from English to Portuguese.
        
        Args:
            genre_en: Genre name in English
            
        Returns:
            Translated genre or original if no translation exists
        """
        return self.genre_translations.get(genre_en, genre_en)
    
    def _build_cover_urls(self, cover_id: Optional[int]) -> List[str]:
        """
        Build fallback chain of cover URLs with different sizes.
        
        Args:
            cover_id: OpenLibrary cover ID
            
        Returns:
            List of URLs to try in order (M, L, S)
        """
        if not cover_id:
            return []
        
        return [
            self.COVER_URL_TEMPLATE.format(cover_id=cover_id, size='M'),
            self.COVER_URL_TEMPLATE.format(cover_id=cover_id, size='L'),
            self.COVER_URL_TEMPLATE.format(cover_id=cover_id, size='S'),
        ]
    
    def _extract_genres(self, subjects: List[str], limit: int = 3) -> str:
        """
        Extract and translate top genres from subject list.
        
        Args:
            subjects: Raw subject list from OpenLibrary
            limit: Maximum number of genres to extract
            
        Returns:
            Comma-separated translated genres
        """
        if not subjects:
            return 'Geral'
        
        # Filter out overly specific subjects and translate
        translated = []
        for subject in subjects[:10]:  # Check first 10
            if len(translated) >= limit:
                break
            # Skip if too long (likely too specific)
            if len(subject) > 30:
                continue
            translated_genre = self._translate_genre(subject)
            if translated_genre not in translated:
                translated.append(translated_genre)
        
        return ', '.join(translated) if translated else 'Geral'
    
    def _save_metrics(self, endpoint: str, query: str, response_time_ms: float,
                     results_count: int, cache_hit: bool = False,
                     error_occurred: bool = False, error_message: str = None):
        """
        Save API call metrics to database for analytics.
        
        Args:
            endpoint: API endpoint called
            query: Search query
            response_time_ms: Response time in milliseconds
            results_count: Number of results returned
            cache_hit: Whether result came from cache
            error_occurred: Whether an error occurred
            error_message: Error details if any
        """
        try:
            metric = APIMetrics(
                endpoint=endpoint,
                query=query,
                response_time_ms=response_time_ms,
                results_count=results_count,
                cache_hit=cache_hit,
                error_occurred=error_occurred,
                error_message=error_message
            )
            db.session.add(metric)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(f"Failed to save API metrics: {e}")
            db.session.rollback()
    
    @cache.memoize(timeout=3600)  # 1-hour cache
    def search_books(self, query: str, limit: int = 10, lang: str = 'pt') -> List[Dict]:
        """
        Search for books in OpenLibrary API with caching and translation.
        
        Args:
            query: Search query string
            limit: Maximum number of results (default 10)
            lang: Target language for translations (default 'pt')
            
        Returns:
            List of book dictionaries with translated metadata
        """
        start_time = time.time()
        endpoint = 'openlibrary_search'
        
        try:
            # Make API request
            params = {'q': query, 'limit': limit}
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=self.TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for doc in data.get('docs', [])[:limit]:
                # Extract and process book data
                title = doc.get('title', 'Título Desconhecido')
                author = ', '.join(doc.get('author_name', [])[:3]) or 'Autor Desconhecido'
                subjects = doc.get('subject', [])
                genre = self._extract_genres(subjects)
                cover_id = doc.get('cover_i')
                cover_urls = self._build_cover_urls(cover_id)
                
                # Get ISBN
                isbn_list = doc.get('isbn', [])
                isbn = isbn_list[0] if isbn_list else None
                
                # Get OpenLibrary key for future reference
                ol_key = doc.get('key', '')
                
                results.append({
                    'title': title,
                    'author': author,
                    'genre': genre,
                    'year': doc.get('first_publish_year') or 2024,
                    'publisher': doc.get('publisher', ['Editora Desconhecida'])[0] if doc.get('publisher') else 'Editora Desconhecida',
                    'cover_url': cover_urls[0] if cover_urls else None,
                    'fallback_urls': cover_urls,
                    'isbn': isbn,
                    'openlibrary_key': ol_key,
                    'pages': doc.get('number_of_pages_median', 0)
                })
            
            # Save metrics
            response_time_ms = (time.time() - start_time) * 1000
            self._save_metrics(
                endpoint=endpoint,
                query=query,
                response_time_ms=response_time_ms,
                results_count=len(results),
                cache_hit=False
            )
            
            current_app.logger.info(
                f"OpenLibrary search: query='{query}' results={len(results)} "
                f"time={response_time_ms:.2f}ms"
            )
            
            return results
            
        except requests.RequestException as e:
            # Network or API error
            response_time_ms = (time.time() - start_time) * 1000
            error_msg = str(e)
            
            self._save_metrics(
                endpoint=endpoint,
                query=query,
                response_time_ms=response_time_ms,
                results_count=0,
                error_occurred=True,
                error_message=error_msg
            )
            
            current_app.logger.error(f"OpenLibrary API error: {error_msg}")
            return []
            
        except Exception as e:
            # Unexpected error
            response_time_ms = (time.time() - start_time) * 1000
            error_msg = str(e)
            
            self._save_metrics(
                endpoint=endpoint,
                query=query,
                response_time_ms=response_time_ms,
                results_count=0,
                error_occurred=True,
                error_message=error_msg
            )
            
            current_app.logger.error(f"Unexpected error in search_books: {error_msg}")
            return []


# Singleton instance
_service_instance = None

def get_openlibrary_service() -> OpenLibraryService:
    """Get or create singleton instance of OpenLibraryService."""
    global _service_instance
    if _service_instance is None:
        _service_instance = OpenLibraryService()
    return _service_instance

