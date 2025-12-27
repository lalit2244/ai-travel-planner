"""
Unit tests for travel planning tools.
"""

import pytest
import json
from src.tools import (
    FlightSearchTool,
    HotelRecommendationTool,
    PlacesDiscoveryTool,
    WeatherLookupTool,
    BudgetEstimationTool
)


class TestFlightSearchTool:
    """Tests for FlightSearchTool."""
    
    def test_flight_search_basic(self):
        """Test basic flight search."""
        tool = FlightSearchTool()
        query = json.dumps({
            "source": "Delhi",
            "destination": "Goa",
            "preference": "cheapest"
        })
        result = tool._run(query)
        assert "Found" in result or "No flights" in result
    
    def test_flight_search_invalid_json(self):
        """Test flight search with invalid JSON."""
        tool = FlightSearchTool()
        result = tool._run("invalid json")
        assert "Error" in result


class TestHotelRecommendationTool:
    """Tests for HotelRecommendationTool."""
    
    def test_hotel_search_basic(self):
        """Test basic hotel search."""
        tool = HotelRecommendationTool()
        query = json.dumps({
            "city": "Goa",
            "min_rating": 4.0
        })
        result = tool._run(query)
        assert "Found" in result or "No hotels" in result
    
    def test_hotel_search_missing_city(self):
        """Test hotel search without city."""
        tool = HotelRecommendationTool()
        query = json.dumps({"min_rating": 4.0})
        result = tool._run(query)
        assert "Error" in result


class TestPlacesDiscoveryTool:
    """Tests for PlacesDiscoveryTool."""
    
    def test_places_search_basic(self):
        """Test basic places search."""
        tool = PlacesDiscoveryTool()
        query = json.dumps({
            "city": "Goa",
            "category": "Beach",
            "min_rating": 4.0
        })
        result = tool._run(query)
        assert "Found" in result or "No places" in result


class TestBudgetEstimationTool:
    """Tests for BudgetEstimationTool."""
    
    def test_budget_calculation(self):
        """Test budget calculation."""
        tool = BudgetEstimationTool()
        query = json.dumps({
            "flight_price": 5000,
            "hotel_price_per_night": 3000,
            "num_nights": 4,
            "daily_expense": 2000
        })
        result = tool._run(query)
        assert "Budget Breakdown" in result
        assert "₹" in result
    
    def test_budget_calculation_invalid_json(self):
        """Test budget calculation with invalid JSON."""
        tool = BudgetEstimationTool()
        result = tool._run("invalid")
        assert "Error" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])