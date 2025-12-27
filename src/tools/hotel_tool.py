"""
Hotel Recommendation Tool for the travel planning agent.
"""

from typing import List, Dict, Any
from langchain.tools import BaseTool
from pydantic import Field
import logging

from config.settings import settings
from src.utils.data_loader import DataLoader, sort_data

logger = logging.getLogger(__name__)


class HotelRecommendationTool(BaseTool):
    """Tool for finding and recommending hotels."""
    
    name: str = "hotel_recommendation"
    description: str = """
    Find hotel recommendations in a city.
    Input should be a JSON string with keys: 'city', optionally 'min_rating' (default 3), 'max_price_per_night'.
    Example: {"city": "Goa", "min_rating": 4, "max_price_per_night": 5000}
    Returns hotel options with name, star rating, price, and amenities.
    """
    
    def _run(self, query: str) -> str:
        """Execute the hotel search."""
        try:
            import json
            params = json.loads(query)
            
            city = params.get("city", "").strip()
            min_rating = int(params.get("min_rating", 3))  # Using stars (1-5)
            max_price = params.get("max_price_per_night")
            
            if not city:
                return "Error: City is required."
            
            # Load hotel data
            hotels = DataLoader.load_json(settings.HOTELS_PATH)
            
            # Filter by city
            filtered_hotels = [
                hotel for hotel in hotels
                if hotel.get("city", "").lower() == city.lower()
            ]
            
            if not filtered_hotels:
                return f"No hotels found in {city}."
            
            # Filter by star rating (using 'stars' field from your data)
            filtered_hotels = [
                hotel for hotel in filtered_hotels
                if hotel.get("stars", 0) >= min_rating
            ]
            
            # Filter by price if specified
            if max_price:
                filtered_hotels = [
                    hotel for hotel in filtered_hotels
                    if hotel.get("price_per_night", float('inf')) <= max_price
                ]
            
            if not filtered_hotels:
                return f"No hotels found in {city} matching your criteria."
            
            # Sort by stars (highest first), then by price (lowest first)
            filtered_hotels = sorted(
                filtered_hotels,
                key=lambda x: (-x.get("stars", 0), x.get("price_per_night", 0))
            )
            
            # Get top 3 options
            top_hotels = filtered_hotels[:3]
            
            # Format output
            result = f"Found {len(filtered_hotels)} hotels in {city} (showing top 3).\n\n"
            result += "Recommended Hotels:\n" + "=" * 50 + "\n"
            
            for i, hotel in enumerate(top_hotels, 1):
                result += f"\nOption {i}:\n"
                result += f"  Name: {hotel.get('name', 'N/A')}\n"
                result += f"  Star Rating: {hotel.get('stars', 0)} ⭐\n"
                result += f"  Price: ₹{hotel.get('price_per_night', 0):,}/night\n"
                
                amenities = hotel.get('amenities', [])
                if amenities:
                    result += f"  Amenities: {', '.join(amenities)}\n"
                
                result += f"  Hotel ID: {hotel.get('hotel_id', 'N/A')}\n"
                result += "-" * 50 + "\n"
            
            return result
            
        except json.JSONDecodeError:
            return "Error: Invalid JSON format. Please provide valid JSON with 'city'."
        except Exception as e:
            logger.error(f"Error in hotel search: {e}")
            return f"Error searching hotels: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async implementation (uses sync version)."""
        return self._run(query)