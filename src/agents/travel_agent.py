"""
Travel Planning Agent using LangChain and Groq.

This module implements the main agentic AI system that orchestrates
all tools to create comprehensive travel itineraries.
"""

from typing import List, Dict, Any
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
import logging

from config.settings import settings
from src.tools import (
    FlightSearchTool,
    HotelRecommendationTool,
    PlacesDiscoveryTool,
    WeatherLookupTool,
    BudgetEstimationTool
)

logger = logging.getLogger(__name__)


class TravelAgent:
    """
    Intelligent travel planning agent that uses multiple tools
    to create personalized itineraries.
    """
    
    def __init__(self):
        """Initialize the travel agent with LLM and tools."""
        self.llm = self._initialize_llm()
        self.tools = self._initialize_tools()
        self.agent_executor = self._create_agent()
    
    def _initialize_llm(self) -> ChatGroq:
        """
        Initialize the Groq LLM.
        
        Returns:
            Configured ChatGroq instance
        """
        return ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_MODEL,
            temperature=settings.MODEL_TEMPERATURE,
            max_tokens=settings.MAX_TOKENS
        )
    
    def _initialize_tools(self) -> List:
        """
        Initialize all tools for the agent.
        
        Returns:
            List of tool instances
        """
        return [
            FlightSearchTool(),
            HotelRecommendationTool(),
            PlacesDiscoveryTool(),
            WeatherLookupTool(),
            BudgetEstimationTool()
        ]
    
    def _create_agent(self) -> AgentExecutor:
        """
        Create the ReAct agent with tools.
        
        Returns:
            Configured AgentExecutor
        """
        # Define the agent prompt
        template = """You are an expert travel planning assistant. Your job is to create comprehensive, 
personalized travel itineraries based on user requirements.

You have access to the following tools:
{tools}

Tool Names: {tool_names}

Use this format:
Thought: Consider what information you need
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action (must be valid JSON)
Observation: the result of the action
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now have enough information to create the final itinerary
Final Answer: [Provide a comprehensive, well-formatted travel itinerary]

IMPORTANT GUIDELINES:
1. Always search for flights first to understand travel costs
2. Find hotels that match the user's budget and preferences
3. Discover places based on user interests and trip duration
4. Check weather for all travel dates
5. Calculate the complete budget breakdown
6. Create a day-wise itinerary with specific places to visit
7. Explain your reasoning for recommendations
8. Format the final answer clearly with sections for:
   - Trip Summary
   - Flight Details
   - Hotel Recommendation
   - Weather Forecast
   - Day-wise Itinerary
   - Budget Breakdown

Previous conversation:
{chat_history}

Current question: {input}
{agent_scratchpad}"""

        prompt = PromptTemplate.from_template(template)
        
        # Create the agent
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        # Create agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=settings.AGENT_VERBOSE,
            max_iterations=settings.AGENT_MAX_ITERATIONS,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )
        
        return agent_executor
    
    def plan_trip(
        self,
        source: str,
        destination: str,
        start_date: str,
        num_days: int,
        budget: int = None,
        preferences: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Plan a complete trip itinerary.
        
        Args:
            source: Source city
            destination: Destination city
            start_date: Start date (YYYY-MM-DD)
            num_days: Number of days
            budget: Total budget (optional)
            preferences: User preferences dict (optional)
            
        Returns:
            Dictionary with itinerary and intermediate steps
        """
        try:
            # Build the query
            query = self._build_query(
                source, destination, start_date, num_days, budget, preferences
            )
            
            logger.info(f"Planning trip: {source} → {destination} for {num_days} days")
            
            # Execute the agent
            result = self.agent_executor.invoke({
                "input": query,
                "chat_history": ""
            })
            
            return {
                "success": True,
                "itinerary": result.get("output", ""),
                "intermediate_steps": result.get("intermediate_steps", []),
                "query": query
            }
            
        except Exception as e:
            logger.error(f"Error planning trip: {e}")
            return {
                "success": False,
                "error": str(e),
                "itinerary": "",
                "intermediate_steps": []
            }
    
    def _build_query(
        self,
        source: str,
        destination: str,
        start_date: str,
        num_days: int,
        budget: int = None,
        preferences: Dict[str, Any] = None
    ) -> str:
        """
        Build a comprehensive query for the agent.
        
        Args:
            source: Source city
            destination: Destination city
            start_date: Start date
            num_days: Number of days
            budget: Total budget
            preferences: User preferences
            
        Returns:
            Formatted query string
        """
        query = f"""Plan a {num_days}-day trip from {source} to {destination} starting on {start_date}.

Requirements:
- Find the best flight options from {source} to {destination}
- Recommend hotels in {destination}
- Suggest places to visit based on interests
- Provide weather forecast for the travel dates
- Create a detailed day-wise itinerary
- Calculate the complete trip budget

"""
        
        if budget:
            query += f"- Total budget constraint: ₹{budget:,}\n"
        
        if preferences:
            query += "\nPreferences:\n"
            if preferences.get("flight_preference"):
                query += f"- Flight: {preferences['flight_preference']}\n"
            if preferences.get("hotel_rating"):
                query += f"- Hotel minimum rating: {preferences['hotel_rating']}⭐\n"
            if preferences.get("interests"):
                query += f"- Interests: {', '.join(preferences['interests'])}\n"
        
        query += "\nPlease provide a comprehensive itinerary with all details."
        
        return query


def create_travel_agent() -> TravelAgent:
    """
    Factory function to create a travel agent instance.
    
    Returns:
        Initialized TravelAgent
    """
    return TravelAgent()


if __name__ == "__main__":
    # Test the travel agent
    print("=" * 60)
    print("Testing Travel Agent")
    print("=" * 60)
    
    agent = create_travel_agent()
    
    result = agent.plan_trip(
        source="Delhi",
        destination="Goa",
        start_date="2025-02-15",
        num_days=5,
        preferences={
            "flight_preference": "cheapest",
            "hotel_rating": 4.0,
            "interests": ["Beach", "Heritage"]
        }
    )
    
    print("\n" + "=" * 60)
    print("RESULT:")
    print("=" * 60)
    print(result["itinerary"])
    print("=" * 60)