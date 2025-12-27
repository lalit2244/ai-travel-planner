"""
Flight Search Tool for the travel planning agent.
"""

from typing import List, Dict, Any, Optional
from langchain.tools import BaseTool
from pydantic import Field
import logging

from config.settings import settings
from src.utils.data_loader import DataLoader, filter_data, sort_data

logger = logging.getLogger(__name__)


class FlightSearchTool(BaseTool):
    """Tool for searching and filtering flights."""
    
    name: str = "flight_search"
    description: str = """
    Search for flights between two cities. 
    Input should be a JSON string with keys: 'source', 'destination', and optionally 'preference' (cheapest/fastest).
    Example: {"source": "Delhi", "destination": "Goa", "preference": "cheapest"}
    Returns flight options with price, duration, airline, and departure time.
    """
    
    def _run(self, query: str) -> str:
        """Execute the flight search."""
        try:
            import json
            params = json.loads(query)
            
            source = params.get("source", "").strip()
            destination = params.get("destination", "").strip()
            preference = params.get("preference", "cheapest").lower()
            
            if not source or not destination:
                return "Error: Both source and destination are required."
            
            # Load flight data
            flights = DataLoader.load_json(settings.FLIGHTS_PATH)
            
            # Filter by source and destination (using 'from' and 'to' fields)
            filtered_flights = [
                flight for flight in flights
                if flight.get("from", "").lower() == source.lower()
                and flight.get("to", "").lower() == destination.lower()
            ]
            
            if not filtered_flights:
                return f"No flights found from {source} to {destination}."
            
            # Calculate duration and sort
            for flight in filtered_flights:
                # If duration not in data, calculate from times
                if "duration_hours" not in flight:
                    try:
                        from datetime import datetime
                        dep = datetime.fromisoformat(flight.get("departure_time", ""))
                        arr = datetime.fromisoformat(flight.get("arrival_time", ""))
                        duration = (arr - dep).total_seconds() / 3600
                        flight["duration_hours"] = round(duration, 1)
                    except:
                        flight["duration_hours"] = 0
            
            # Sort based on preference
            if preference == "fastest":
                filtered_flights = sorted(filtered_flights, key=lambda x: x.get("duration_hours", 999))
            else:  # Default to cheapest
                filtered_flights = sorted(filtered_flights, key=lambda x: x.get("price", 999999))
            
            # Get top 3 options
            top_flights = filtered_flights[:3]
            
            # Format output
            result = f"Found {len(filtered_flights)} flights from {source} to {destination}.\n\n"
            result += "Top 3 Options:\n" + "=" * 50 + "\n"
            
            for i, flight in enumerate(top_flights, 1):
                result += f"\nOption {i}:\n"
                result += f"  Airline: {flight.get('airline', 'N/A')}\n"
                result += f"  Price: ₹{flight.get('price', 0):,}\n"
                result += f"  Duration: {flight.get('duration_hours', 0)} hours\n"
                
                dep_time = flight.get('departure_time', 'N/A')
                if 'T' in str(dep_time):
                    dep_time = dep_time.split('T')[1][:5]  # Extract time only
                result += f"  Departure: {dep_time}\n"
                
                result += f"  Flight ID: {flight.get('flight_id', 'N/A')}\n"
                result += "-" * 50 + "\n"
            
            return result
            
        except json.JSONDecodeError:
            return "Error: Invalid JSON format."
        except Exception as e:
            logger.error(f"Error in flight search: {e}")
            return f"Error searching flights: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async implementation."""
        return self._run(query)