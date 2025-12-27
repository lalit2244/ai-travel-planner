"""
Data loading utilities with caching for improved performance.

This module provides efficient JSON data loading with in-memory caching
to avoid repeated file I/O operations.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from functools import lru_cache
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """
    Handles loading and caching of JSON data files.
    
    Uses LRU caching to improve performance by avoiding repeated file reads.
    """
    
    _cache = {}
    
    @classmethod
    def load_json(cls, file_path: Path) -> List[Dict[str, Any]]:
        """
        Load JSON data from file with caching.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            List of dictionaries containing the JSON data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        # Convert to string for caching
        file_path_str = str(file_path)
        
        # Check cache first
        if file_path_str in cls._cache:
            logger.debug(f"Loading {file_path.name} from cache")
            return cls._cache[file_path_str]
        
        # Load from file
        try:
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                raise FileNotFoundError(f"Data file not found: {file_path}")
            
            logger.info(f"Loading {file_path.name} from disk")
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Cache the data
            cls._cache[file_path_str] = data
            logger.info(f"Successfully loaded {len(data)} records from {file_path.name}")
            
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            raise
    
    @classmethod
    def clear_cache(cls) -> None:
        """Clear the data cache."""
        cls._cache.clear()
        logger.info("Data cache cleared")
    
    @classmethod
    def get_cache_info(cls) -> Dict[str, int]:
        """
        Get information about cached data.
        
        Returns:
            Dictionary with cache statistics
        """
        return {
            "cached_files": len(cls._cache),
            "total_records": sum(len(data) for data in cls._cache.values())
        }


def filter_data(
    data: List[Dict[str, Any]],
    filters: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Filter a list of dictionaries based on provided criteria.
    
    Args:
        data: List of dictionaries to filter
        filters: Dictionary of field:value pairs to filter by
        
    Returns:
        Filtered list of dictionaries
        
    Example:
        >>> flights = [{"source": "Delhi", "price": 5000}, ...]
        >>> filtered = filter_data(flights, {"source": "Delhi"})
    """
    if not filters:
        return data
    
    filtered = data
    for key, value in filters.items():
        if value is not None:
            filtered = [
                item for item in filtered
                if key in item and str(item[key]).lower() == str(value).lower()
            ]
    
    return filtered


def sort_data(
    data: List[Dict[str, Any]],
    sort_by: str,
    reverse: bool = False
) -> List[Dict[str, Any]]:
    """
    Sort a list of dictionaries by a specific field.
    
    Args:
        data: List of dictionaries to sort
        sort_by: Field name to sort by
        reverse: If True, sort in descending order
        
    Returns:
        Sorted list of dictionaries
    """
    try:
        return sorted(
            data,
            key=lambda x: x.get(sort_by, float('inf')),
            reverse=reverse
        )
    except TypeError:
        # Handle cases where values can't be compared directly
        logger.warning(f"Could not sort by {sort_by}, returning original order")
        return data


def get_unique_values(
    data: List[Dict[str, Any]],
    field: str
) -> List[Any]:
    """
    Get unique values for a specific field in the data.
    
    Args:
        data: List of dictionaries
        field: Field name to extract unique values from
        
    Returns:
        List of unique values
    """
    values = set()
    for item in data:
        if field in item:
            values.add(item[field])
    
    return sorted(list(values))


if __name__ == "__main__":
    # Test the data loader
    from config.settings import settings
    
    print("=" * 60)
    print("Testing DataLoader")
    print("=" * 60)
    
    try:
        # Test loading flights
        flights = DataLoader.load_json(settings.FLIGHTS_PATH)
        print(f"✓ Loaded {len(flights)} flights")
        
        # Test loading hotels
        hotels = DataLoader.load_json(settings.HOTELS_PATH)
        print(f"✓ Loaded {len(hotels)} hotels")
        
        # Test loading places
        places = DataLoader.load_json(settings.PLACES_PATH)
        print(f"✓ Loaded {len(places)} places")
        
        # Show cache info
        cache_info = DataLoader.get_cache_info()
        print(f"\nCache Info: {cache_info}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("=" * 60)