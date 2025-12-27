"""
Places Discovery Tool for the travel planning agent.
"""

from typing import List, Dict, Any
from langchain.tools import BaseTool
from pydantic import Field
import logging

from config.settings import settings
from src.utils.data_loader import DataLoader, sort_data

logger = logging.getLogger(__name__)


class PlacesDiscoveryTool(BaseTool):
    """Tool for discovering tourist attractions and places of interest."""
    
    name: str = "places_discovery"
    description: str = """
    Discover tourist attractions and places to visit in a city.
    Input should be a JSON string with keys: 'city', optionally 'category' and 'min_rating'.
    Example: {"city": "Goa", "category": "beach", "min_rating": 4.0}
    Returns places with name, category, rating, and description.
    """
    
    def _run(self, query: str) -> str:
        """Execute the places search."""
        try:
            import json
            params = json.loads(query)
            
            city = params.get("city", "").strip()
            category = params.get("category", "").strip().lower()
            min_rating = float(params.get("min_rating", 3.5))
            
            if not city:
                return "Error: City is required."
            
            # Load places data
            places = DataLoader.load_json(settings.PLACES_PATH)
            
            # Filter by city
            filtered_places = [
                place for place in places
                if place.get("city", "").lower() == city.lower()
            ]
            
            if not filtered_places:
                return f"No places found in {city}."
            
            # Filter by category if specified (using 'type' field)
            if category:
                filtered_places = [
                    place for place in filtered_places
                    if place.get("type", "").lower() == category.lower()
                ]
            
            # Filter by rating
            filtered_places = [
                place for place in filtered_places
                if place.get("rating", 0) >= min_rating
            ]
            
            if not filtered_places:
                criteria = f" in category '{category}'" if category else ""
                return f"No places found in {city}{criteria} matching your criteria."
            
            # Sort by rating (highest first)
            filtered_places = sorted(
                filtered_places,
                key=lambda x: -x.get("rating", 0)
            )
            
            # Get top 5 options
            top_places = filtered_places[:5]
            
            # Format output
            category_text = f" ({category})" if category else ""
            result = f"Found {len(filtered_places)} places in {city}{category_text} (showing top 5).\n\n"
            result += "Recommended Places:\n" + "=" * 50 + "\n"
            
            for i, place in enumerate(top_places, 1):
                result += f"\n{i}. {place.get('name', 'N/A')}\n"
                result += f"   Category: {place.get('type', 'N/A')}\n"
                result += f"   Rating: {place.get('rating', 0)}⭐\n"
                
                description = place.get('description', '')
                if description:
                    result += f"   Description: {description}\n"
                
                result += f"   Place ID: {place.get('place_id', 'N/A')}\n"
                result += "-" * 50 + "\n"
            
            return result
            
        except json.JSONDecodeError:
            return "Error: Invalid JSON format."
        except Exception as e:
            logger.error(f"Error in places search: {e}")
            return f"Error searching places: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async implementation."""
        return self._run(query)