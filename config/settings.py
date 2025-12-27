"""
Configuration settings for the AI Travel Planning Assistant.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory of the project - more robust detection
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:
    """Application settings and configuration parameters."""
    
    # ==================== API Configuration ====================
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    # Model Parameters
    MODEL_TEMPERATURE: float = float(os.getenv("MODEL_TEMPERATURE", "0.3"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "4096"))
    
    # ==================== File Paths ====================
    # Use absolute paths to ensure files are found
    DATA_PATH: Path = BASE_DIR / "data"
    FLIGHTS_FILE: str = "flights.json"
    HOTELS_FILE: str = "hotels.json"
    PLACES_FILE: str = "places.json"
    
    # Full file paths - using absolute paths
    FLIGHTS_PATH: Path = DATA_PATH / FLIGHTS_FILE
    HOTELS_PATH: Path = DATA_PATH / HOTELS_FILE
    PLACES_PATH: Path = DATA_PATH / PLACES_FILE
    
    # ==================== Weather API ====================
    WEATHER_API_URL: str = os.getenv(
        "WEATHER_API_URL",
        "https://api.open-meteo.com/v1/forecast"
    )
    
    # ==================== Budget Settings ====================
    DEFAULT_DAILY_EXPENSE: int = int(os.getenv("DEFAULT_DAILY_EXPENSE", "2000"))
    MIN_TRIP_DAYS: int = int(os.getenv("MIN_TRIP_DAYS", "3"))
    MAX_TRIP_DAYS: int = int(os.getenv("MAX_TRIP_DAYS", "7"))
    
    # ==================== Agent Configuration ====================
    AGENT_MAX_ITERATIONS: int = int(os.getenv("AGENT_MAX_ITERATIONS", "15"))
    AGENT_VERBOSE: bool = os.getenv("AGENT_VERBOSE", "True").lower() == "true"
    
    # ==================== Application Settings ====================
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # ==================== City Coordinates (for weather API) ====================
    CITY_COORDINATES = {
        "mumbai": {"latitude": 19.0760, "longitude": 72.8777},
        "delhi": {"latitude": 28.7041, "longitude": 77.1025},
        "bangalore": {"latitude": 12.9716, "longitude": 77.5946},
        "kolkata": {"latitude": 22.5726, "longitude": 88.3639},
        "chennai": {"latitude": 13.0827, "longitude": 80.2707},
        "hyderabad": {"latitude": 17.3850, "longitude": 78.4867},
        "pune": {"latitude": 18.5204, "longitude": 73.8567},
        "ahmedabad": {"latitude": 23.0225, "longitude": 72.5714},
        "jaipur": {"latitude": 26.9124, "longitude": 75.7873},
        "goa": {"latitude": 15.2993, "longitude": 74.1240},
        "kochi": {"latitude": 9.9312, "longitude": 76.2673},
        "udaipur": {"latitude": 24.5854, "longitude": 73.7125},
        "varanasi": {"latitude": 25.3176, "longitude": 82.9739},
        "shimla": {"latitude": 31.1048, "longitude": 77.1734},
        "manali": {"latitude": 32.2432, "longitude": 77.1892},
        "darjeeling": {"latitude": 27.0410, "longitude": 88.2663},
        "agra": {"latitude": 27.1767, "longitude": 78.0081},
        "amritsar": {"latitude": 31.6340, "longitude": 74.8723},
        "mysore": {"latitude": 12.2958, "longitude": 76.6394},
        "rishikesh": {"latitude": 30.0869, "longitude": 78.2676},
    }
    
    # ==================== UI Configuration ====================
    STREAMLIT_PAGE_TITLE = "AI Travel Planner"
    STREAMLIT_PAGE_ICON = "✈️"
    STREAMLIT_LAYOUT = "wide"
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate that all required settings are properly configured.
        
        Returns:
            bool: True if all settings are valid, raises ValueError otherwise
        """
        print(f"BASE_DIR: {BASE_DIR}")
        print(f"DATA_PATH: {cls.DATA_PATH}")
        print(f"DATA_PATH exists: {cls.DATA_PATH.exists()}")
        
        if not cls.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not set. Please add it to your .env file.\n"
                "Get your free API key from: https://console.groq.com"
            )
        
        # Check if data directory exists
        if not cls.DATA_PATH.exists():
            cls.DATA_PATH.mkdir(parents=True, exist_ok=True)
            print(f"Created data directory: {cls.DATA_PATH}")
        
        # Check each data file
        for name, path in [
            ("Flights", cls.FLIGHTS_PATH),
            ("Hotels", cls.HOTELS_PATH),
            ("Places", cls.PLACES_PATH)
        ]:
            if not path.exists():
                print(f"WARNING: {name} file not found at: {path}")
            else:
                print(f"✓ {name} file found: {path}")
        
        return True
    
    @classmethod
    def get_city_coordinates(cls, city: str) -> Optional[dict]:
        """
        Get coordinates for a given city.
        
        Args:
            city: City name
            
        Returns:
            Dictionary with latitude and longitude, or None if city not found
        """
        return cls.CITY_COORDINATES.get(city.lower())


# Create a singleton instance
settings = Settings()

# Validate settings on import
try:
    settings.validate()
except ValueError as e:
    print(f"⚠️  Configuration Error: {e}")


if __name__ == "__main__":
    # Test configuration
    print("=" * 60)
    print("AI Travel Planner - Configuration")
    print("=" * 60)
    print(f"Groq API Key: {'✓ Set' if settings.GROQ_API_KEY else '✗ Not Set'}")
    print(f"Model: {settings.GROQ_MODEL}")
    print(f"Base Directory: {BASE_DIR}")
    print(f"Data Path: {settings.DATA_PATH}")
    print(f"Data Path Exists: {settings.DATA_PATH.exists()}")
    print()
    print(f"Flights Path: {settings.FLIGHTS_PATH}")
    print(f"Flights Data Exists: {settings.FLIGHTS_PATH.exists()}")
    print()
    print(f"Hotels Path: {settings.HOTELS_PATH}")
    print(f"Hotels Data Exists: {settings.HOTELS_PATH.exists()}")
    print()
    print(f"Places Path: {settings.PLACES_PATH}")
    print(f"Places Data Exists: {settings.PLACES_PATH.exists()}")
    print("=" * 60)
    
    # Try to load one file
    if settings.FLIGHTS_PATH.exists():
        import json
        with open(settings.FLIGHTS_PATH, 'r') as f:
            flights = json.load(f)
        print(f"\n✓ Successfully loaded {len(flights)} flights from JSON")
    else:
        print("\n✗ Could not load flights file")