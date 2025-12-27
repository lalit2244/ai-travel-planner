"""
Budget Estimation Tool for the travel planning agent.

This tool calculates the total trip budget including flights, hotels,
and daily expenses.
"""

from typing import Dict, Any
from langchain.tools import BaseTool
from pydantic import Field
import logging

from config.settings import settings

logger = logging.getLogger(__name__)


class BudgetEstimationTool(BaseTool):
    """
    Tool for calculating trip budget.
    
    Calculates total cost including flight, hotel, and daily expenses.
    """
    
    name: str = "budget_estimation"
    description: str = """
    Calculate total trip budget.
    Input should be a JSON string with keys: 'flight_price', 'hotel_price_per_night', 'num_nights', 'daily_expense' (optional).
    Example: {"flight_price": 4800, "hotel_price_per_night": 3200, "num_nights": 4, "daily_expense": 2000}
    Returns detailed budget breakdown with total cost.
    """
    
    def _run(self, query: str) -> str:
        """
        Execute the budget calculation.
        
        Args:
            query: JSON string with cost parameters
            
        Returns:
            Formatted string with budget breakdown
        """
        try:
            import json
            params = json.loads(query)
            
            flight_price = float(params.get("flight_price", 0))
            hotel_price_per_night = float(params.get("hotel_price_per_night", 0))
            num_nights = int(params.get("num_nights", 1))
            daily_expense = float(params.get("daily_expense", settings.DEFAULT_DAILY_EXPENSE))
            
            # Calculate costs
            hotel_total = hotel_price_per_night * num_nights
            food_travel_total = daily_expense * (num_nights + 1)  # +1 for arrival day
            total_cost = flight_price + hotel_total + food_travel_total
            
            # Format output
            result = "Budget Breakdown\n"
            result += "=" * 50 + "\n\n"
            result += f"✈️  Flight Cost:          ₹{flight_price:,.0f}\n"
            result += f"🏨 Hotel ({num_nights} nights):  ₹{hotel_total:,.0f}\n"
            result += f"    (₹{hotel_price_per_night:,.0f} per night)\n"
            result += f"🍽️  Food & Local Travel:  ₹{food_travel_total:,.0f}\n"
            result += f"    (₹{daily_expense:,.0f} per day × {num_nights + 1} days)\n"
            result += "\n" + "-" * 50 + "\n"
            result += f"💰 Total Estimated Cost: ₹{total_cost:,.0f}\n"
            result += "=" * 50 + "\n"
            
            # Add budget tips
            result += "\n💡 Budget Tips:\n"
            if total_cost > 30000:
                result += "   • Consider booking in advance for better rates\n"
            if hotel_price_per_night > 4000:
                result += "   • Look for hotels slightly away from tourist hotspots\n"
            result += "   • Use local transport to save on daily expenses\n"
            result += "   • Try local eateries for authentic and affordable food\n"
            
            return result
            
        except json.JSONDecodeError:
            return "Error: Invalid JSON format."
        except Exception as e:
            logger.error(f"Error in budget calculation: {e}")
            return f"Error calculating budget: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async implementation (uses sync version)."""
        return self._run(query)


def calculate_budget(
    flight_price: float,
    hotel_price_per_night: float,
    num_nights: int,
    daily_expense: float = None
) -> Dict[str, float]:
    """
    Helper function to calculate budget programmatically.
    
    Args:
        flight_price: Cost of flight
        hotel_price_per_night: Hotel cost per night
        num_nights: Number of nights
        daily_expense: Daily expense for food and travel
        
    Returns:
        Dictionary with budget breakdown
    """
    if daily_expense is None:
        daily_expense = settings.DEFAULT_DAILY_EXPENSE
    
    hotel_total = hotel_price_per_night * num_nights
    food_travel_total = daily_expense * (num_nights + 1)
    total_cost = flight_price + hotel_total + food_travel_total
    
    return {
        "flight_cost": flight_price,
        "hotel_cost": hotel_total,
        "food_travel_cost": food_travel_total,
        "total_cost": total_cost,
        "per_day_average": total_cost / (num_nights + 1)
    }


def estimate_daily_expense(destination_city: str) -> float:
    """
    Estimate daily expense based on destination.
    
    Args:
        destination_city: Name of destination city
        
    Returns:
        Estimated daily expense in INR
    """
    # Tier-based pricing
    tier_1_cities = ["mumbai", "delhi", "bangalore"]
    tier_2_cities = ["goa", "jaipur", "udaipur", "shimla", "manali"]
    
    city_lower = destination_city.lower()
    
    if city_lower in tier_1_cities:
        return 2500
    elif city_lower in tier_2_cities:
        return 2000
    else:
        return 1500


if __name__ == "__main__":
    # Test the budget estimation tool
    print("=" * 60)
    print("Testing Budget Estimation Tool")
    print("=" * 60)
    
    tool = BudgetEstimationTool()
    
    # Test query
    test_query = '{"flight_price": 4800, "hotel_price_per_night": 3200, "num_nights": 4, "daily_expense": 2000}'
    result = tool._run(test_query)
    print(result)
    
    print("\n" + "=" * 60)
    print("Testing Helper Function")
    print("=" * 60)
    budget = calculate_budget(4800, 3200, 4, 2000)
    print(budget)
    
    print("=" * 60)