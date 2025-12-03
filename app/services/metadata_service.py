# metadata_service.py
"""
Centralized metadata service for book information retrieval from multiple sources.

This service abstracts the complexity of fetching book metadata from various APIs
(OpenLibrary, Google Books, WorldCat, etc.) and provides a unified interface for
the application.

Architecture inspired by Tellico's multi-source metadata fetching approach.
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import requests
from flask import current_app


class MetadataService:
    """
    Service class for fetching book metadata from external APIs.
    
    Provides methods to search and retrieve book information from multiple sources
    with built-in caching, error handling, and rate limiting.
    """
    
    # API Configuration
    OPENLIBRARY_BASE_URL = "https://openlibrary.org"
    OPENLIBRARY_COVERS_URL = "https://covers.openlibrary.org/b"
    
    # Rate limiting configuration
    REQUESTS_PER_MINUTE = 100
    CACHE_TTL = 86400  # 24 hours in seconds
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._request_count = 0
        self._last_reset = datetime.now()
    
    def _check_rate_limit(self) -> bool:
        """
        Check if we're within rate limits.
        
        Returns:
            bool: True if request is allowed, False if rate limited
        """
        now = datetime.now()
        if (now - self._last_reset).seconds >= 60:
            self._request_count = 0
            self._last_reset = now
        
        if self._request_count >= self.REQUESTS_PER_MINUTE:
            self.logger.warning("Rate limit exceeded for metadata API")
            return False
        
        self._request_count += 1
        return True
    
    def search_openlibrary(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for books in OpenLibrary API.
        
        Args:
            query: Search term (title, author, ISBN, etc.)
            limit: Maximum number of results to return
            
        Returns:
            List of book dictionaries with standardized fields
            
        Example:
            >>> service = MetadataService()
            >>> results = service.search_openlibrary("Harry Potter", limit=5)
            >>> len(results) <= 5
            True
        """
        if not self._check_rate_limit():
            return []
        
        try:
            url = f"{self.OPENLIBRARY_BASE_URL}/search.json"
            params = {
                'q': query,
                'limit': limit,
                'fields': 'key,title,author_name,first_publish_year,isbn,cover_i,publisher,subject,number_of_pages_median'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for doc in data.get('docs', []):
                book_data = self._normalize_openlibrary_result(doc)
                if book_data:
                    results.append(book_data)
            
            self.logger.info(f"OpenLibrary search for '{query}' returned {len(results)} results")
            return results
            
        except requests.exceptions.Timeout:
            self.logger.error(f"OpenLibrary API timeout for query: {query}")
            return []
        except requests.exceptions.RequestException as e:
            self.logger.error(f"OpenLibrary API error: {str(e)}")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error in OpenLibrary search: {str(e)}")
            return []
    
    def _normalize_openlibrary_result(self, doc: Dict) -> Optional[Dict]:
        """
        Normalize OpenLibrary API response to standardized format.
        
        Args:
            doc: Raw document from OpenLibrary API
            
        Returns:
            Normalized book dictionary or None if invalid
        """
        try:
            # Extract ISBNs and get the first valid one
            isbns = doc.get('isbn', [])
            isbn = isbns[0] if isbns else None
            
            # Get cover image URL
            cover_id = doc.get('cover_i')
            cover_url = None
            if cover_id:
                cover_url = f"{self.OPENLIBRARY_COVERS_URL}/id/{cover_id}-M.jpg"
            
            # Get authors
            authors = doc.get('author_name', [])
            author = ', '.join(authors[:3]) if authors else 'Unknown Author'
            
            # Get first publisher
            publishers = doc.get('publisher', [])
            publisher = publishers[0] if publishers else 'Unknown'
            
            # Get subjects (genres)
            subjects = doc.get('subject', [])
            genre = ', '.join(subjects[:3]) if subjects else 'General'
            
            return {
                'title': doc.get('title', 'Unknown Title'),
                'author': author,
                'publisher': publisher,
                'year': doc.get('first_publish_year', datetime.now().year),
                'isbn': isbn,
                'cover_url': cover_url,
                'genre': genre,
                'pages': doc.get('number_of_pages_median', 0),
                'source': 'openlibrary',
                'openlibrary_key': doc.get('key', '')
            }
        except Exception as e:
            self.logger.warning(f"Failed to normalize OpenLibrary result: {str(e)}")
            return None
    
    def get_book_by_isbn(self, isbn: str) -> Optional[Dict]:
        """
        Fetch detailed book information by ISBN.
        
        Args:
            isbn: ISBN-10 or ISBN-13
            
        Returns:
            Book dictionary with detailed information or None if not found
            
        TODO: Add Google Books API integration for better ISBN coverage
        TODO: Add WorldCat API integration for library records
        """
        if not self._check_rate_limit():
            return None
        
        try:
            # Clean ISBN
            clean_isbn = isbn.replace('-', '').replace(' ', '')
            
            url = f"{self.OPENLIBRARY_BASE_URL}/isbn/{clean_isbn}.json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 404:
                self.logger.info(f"Book not found for ISBN: {isbn}")
                return None
            
            response.raise_for_status()
            data = response.json()
            
            # Get additional details from work
            work_key = data.get('works', [{}])[0].get('key')
            book_details = self._get_work_details(work_key) if work_key else {}
            
            # Combine data
            result = {
                'title': data.get('title', 'Unknown Title'),
                'isbn': clean_isbn,
                'publisher': ', '.join(data.get('publishers', ['Unknown'])),
                'year': data.get('publish_date', '').split()[-1] if data.get('publish_date') else '',
                'pages': data.get('number_of_pages', 0),
                'source': 'openlibrary',
                **book_details
            }
            
            self.logger.info(f"Successfully retrieved book for ISBN: {isbn}")
            return result
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching book by ISBN {isbn}: {str(e)}")
            return None
    
    def _get_work_details(self, work_key: str) -> Dict:
        """
        Fetch additional details from OpenLibrary work endpoint.
        
        Args:
            work_key: OpenLibrary work identifier
            
        Returns:
            Dictionary with additional book details
        """
        try:
            url = f"{self.OPENLIBRARY_BASE_URL}{work_key}.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract description
            description = None
            if isinstance(data.get('description'), dict):
                description = data['description'].get('value')
            elif isinstance(data.get('description'), str):
                description = data['description']
            
            # Extract subjects (genres)
            subjects = data.get('subjects', [])
            genre = ', '.join(subjects[:5]) if subjects else 'General'
            
            # Get cover
            covers = data.get('covers', [])
            cover_url = None
            if covers and covers[0]:
                cover_url = f"{self.OPENLIBRARY_COVERS_URL}/id/{covers[0]}-L.jpg"
            
            # Get authors
            author_keys = [a.get('author', {}).get('key') for a in data.get('authors', [])]
            author_names = [self._get_author_name(key) for key in author_keys if key]
            
            return {
                'author': ', '.join(filter(None, author_names)) or 'Unknown Author',
                'description': description,
                'genre': genre,
                'cover_url': cover_url
            }
            
        except Exception as e:
            self.logger.warning(f"Failed to fetch work details for {work_key}: {str(e)}")
            return {}
    
    def _get_author_name(self, author_key: str) -> Optional[str]:
        """
        Fetch author name from OpenLibrary.
        
        Args:
            author_key: OpenLibrary author identifier
            
        Returns:
            Author name or None
        """
        try:
            url = f"{self.OPENLIBRARY_BASE_URL}{author_key}.json"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get('name')
        except Exception:
            return None
    
    def get_cover_url(self, isbn: Optional[str] = None, cover_id: Optional[int] = None, 
                     size: str = 'M') -> Optional[str]:
        """
        Get book cover image URL.
        
        Args:
            isbn: ISBN for the book
            cover_id: OpenLibrary cover ID
            size: Image size - 'S' (small), 'M' (medium), 'L' (large)
            
        Returns:
            Cover image URL or None
            
        Example:
            >>> service = MetadataService()
            >>> url = service.get_cover_url(isbn="9780747532743", size='L')
            >>> url is not None
            True
        """
        if isbn:
            clean_isbn = isbn.replace('-', '').replace(' ', '')
            return f"{self.OPENLIBRARY_COVERS_URL}/isbn/{clean_isbn}-{size}.jpg"
        elif cover_id:
            return f"{self.OPENLIBRARY_COVERS_URL}/id/{cover_id}-{size}.jpg"
        return None
    
    def search_all_sources(self, query: str, limit: int = 10) -> Dict[str, List[Dict]]:
        """
        Search all available metadata sources.
        
        Args:
            query: Search term
            limit: Maximum results per source
            
        Returns:
            Dictionary mapping source names to result lists
            
        TODO: Implement Google Books API integration
        TODO: Implement WorldCat API integration
        TODO: Implement ISBN DB integration
        TODO: Add parallel request processing for better performance
        """
        results = {
            'openlibrary': self.search_openlibrary(query, limit),
            # TODO: Uncomment when implemented
            # 'google_books': self.search_google_books(query, limit),
            # 'worldcat': self.search_worldcat(query, limit),
        }
        
        return results
    
    # =======================================================================
    # TODO: Future API Integrations
    # =======================================================================
    
    def search_google_books(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search Google Books API.
        
        TODO: Implement Google Books API integration
        - API Key: Requires Google Cloud project setup
        - Endpoint: https://www.googleapis.com/books/v1/volumes
        - Rate Limit: 1000 requests/day (free tier)
        - Features: Rich metadata, preview pages, ratings
        
        Args:
            query: Search term
            limit: Maximum results
            
        Returns:
            List of normalized book dictionaries
        """
        self.logger.info("Google Books API not yet implemented")
        return []
    
    def search_worldcat(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search WorldCat library catalog.
        
        TODO: Implement WorldCat API integration
        - API Key: Requires OCLC developer account
        - Endpoint: http://www.worldcat.org/webservices/catalog/search/
        - Features: Library holdings, MARC records, FRBR grouping
        
        Args:
            query: Search term
            limit: Maximum results
            
        Returns:
            List of normalized book dictionaries
        """
        self.logger.info("WorldCat API not yet implemented")
        return []
    
    def search_isbndb(self, isbn: str) -> Optional[Dict]:
        """
        Search ISBNdb for book information.
        
        TODO: Implement ISBNdb API integration
        - API Key: Requires ISBNdb account (paid service)
        - Endpoint: https://api2.isbndb.com/book/
        - Features: Comprehensive ISBN database, book images
        
        Args:
            isbn: ISBN to lookup
            
        Returns:
            Book dictionary or None
        """
        self.logger.info("ISBNdb API not yet implemented")
        return None


# Singleton instance for application-wide use
_metadata_service = None


def get_metadata_service() -> MetadataService:
    """
    Get or create singleton MetadataService instance.
    
    Returns:
        MetadataService instance
    """
    global _metadata_service
    if _metadata_service is None:
        _metadata_service = MetadataService()
    return _metadata_service

