"""
Weather Lookup Tool for the travel planning agent.

This tool fetches real-time weather forecasts using the Open-Meteo API.
"""

from typing import Dict, Any, List
from langchain.tools import BaseTool
from datetime import datetime, timedelta
import requests
import logging

from config.settings import settings

logger = logging.getLogger(__name__)


class WeatherLookupTool(BaseTool):
    """
    Tool for fetching weather forecasts.
    
    Uses the free Open-Meteo API to get weather information for specific dates.
    """
    
    name: str = "weather_lookup"
    description: str = """
    Get weather forecast for a city and date range.
    Input should be a JSON string with keys: 'city', 'start_date' (YYYY-MM-DD), 'num_days'.
    Example: {"city": "Goa", "start_date": "2025-02-15", "num_days": 5}
    Returns daily weather forecast with temperature and conditions.
    """
    
    def _run(self, query: str) -> str:
        """
        Execute the weather lookup.
        
        Args:
            query: JSON string with search parameters
            
        Returns:
            Formatted string with weather forecast
        """
        try:
            import json
            params = json.loads(query)
            
            city = params.get("city", "").strip()
            start_date = params.get("start_date", "").strip()
            num_days = int(params.get("num_days", 7))
            
            if not city or not start_date:
                return "Error: Both city and start_date are required."
            
            # Get coordinates for the city
            coords = settings.get_city_coordinates(city)
            if not coords:
                return f"Error: Coordinates not found for {city}. Please check the city name."
            
            # Fetch weather data
            weather_data = fetch_weather(
                coords["latitude"],
                coords["longitude"],
                start_date,
                num_days
            )
            
            if not weather_data:
                return f"Error: Could not fetch weather data for {city}."
            
            # Format output
            result = f"Weather Forecast for {city.title()}\n"
            result += f"From {start_date} ({num_days} days)\n"
            result += "=" * 50 + "\n\n"
            
            for day_info in weather_data:
                date = day_info["date"]
                temp_max = day_info["temp_max"]
                temp_min = day_info["temp_min"]
                condition = day_info["condition"]
                
                result += f"📅 {date}:\n"
                result += f"   🌡️  Temperature: {temp_min}°C - {temp_max}°C\n"
                result += f"   {condition}\n"
                result += "-" * 50 + "\n"
            
            return result
            
        except json.JSONDecodeError:
            return "Error: Invalid JSON format."
        except Exception as e:
            logger.error(f"Error in weather lookup: {e}")
            return f"Error fetching weather: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async implementation (uses sync version)."""
        return self._run(query)


def fetch_weather(
    latitude: float,
    longitude: float,
    start_date: str,
    num_days: int = 7
) -> List[Dict[str, Any]]:
    """
    Fetch weather data from Open-Meteo API.
    
    Args:
        latitude: Location latitude
        longitude: Location longitude
        start_date: Start date in YYYY-MM-DD format
        num_days: Number of days to forecast
        
    Returns:
        List of daily weather dictionaries
    """
    try:
        # Parse start date
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = start + timedelta(days=num_days - 1)
        
        # Build API URL
        url = settings.WEATHER_API_URL
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max",
            "timezone": "auto",
            "start_date": start.strftime("%Y-%m-%d"),
            "end_date": end.strftime("%Y-%m-%d")
        }
        
        # Make API request
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Parse response
        daily = data.get("daily", {})
        dates = daily.get("time", [])
        temp_max = daily.get("temperature_2m_max", [])
        temp_min = daily.get("temperature_2m_min", [])
        precipitation = daily.get("precipitation_sum", [])
        windspeed = daily.get("windspeed_10m_max", [])
        
        # Format weather data
        weather_list = []
        for i in range(len(dates)):
            # Determine weather condition
            condition = get_weather_condition(
                precipitation[i] if i < len(precipitation) else 0,
                windspeed[i] if i < len(windspeed) else 0
            )
            
            weather_list.append({
                "date": dates[i],
                "temp_max": round(temp_max[i]) if i < len(temp_max) else None,
                "temp_min": round(temp_min[i]) if i < len(temp_min) else None,
                "precipitation": round(precipitation[i], 1) if i < len(precipitation) else 0,
                "windspeed": round(windspeed[i], 1) if i < len(windspeed) else 0,
                "condition": condition
            })
        
        return weather_list
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request error: {e}")
        return []
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        return []


def get_weather_condition(precipitation: float, windspeed: float) -> str:
    """
    Determine weather condition based on precipitation and wind.
    
    Args:
        precipitation: Precipitation in mm
        windspeed: Wind speed in km/h
        
    Returns:
        Weather condition emoji and description
    """
    if precipitation > 10:
        return "🌧️  Rainy"
    elif precipitation > 2:
        return "🌦️  Light Rain"
    elif windspeed > 30:
        return "💨  Windy"
    elif windspeed > 15:
        return "🌤️  Breezy"
    else:
        return "☀️  Clear/Sunny"


if __name__ == "__main__":
    # Test the weather lookup tool
    print("=" * 60)
    print("Testing Weather Lookup Tool")
    print("=" * 60)
    
    tool = WeatherLookupTool()
    
    # Test query
    test_query = '{"city": "Goa", "start_date": "2025-02-15", "num_days": 5}'
    result = tool._run(test_query)
    print(result)
    
    print("=" * 60)