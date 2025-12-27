"""
AI Travel Planning Assistant - Streamlit Application
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, Any, List
import json
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Direct imports
from config.settings import settings

# Import agent components directly
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

from src.tools.flight_tool import FlightSearchTool
from src.tools.hotel_tool import HotelRecommendationTool
from src.tools.places_tool import PlacesDiscoveryTool
from src.tools.weather_tool import WeatherLookupTool
from src.tools.budget_tool import BudgetEstimationTool
from src.utils.data_loader import DataLoader

# Quick test on startup
print("=" * 60)
print("STARTUP TEST")
print("=" * 60)
try:
    test_flights = DataLoader.load_json(settings.FLIGHTS_PATH)
    test_hotels = DataLoader.load_json(settings.HOTELS_PATH)
    test_places = DataLoader.load_json(settings.PLACES_PATH)
    print(f"✓ Loaded {len(test_flights)} flights")
    print(f"✓ Loaded {len(test_hotels)} hotels")
    print(f"✓ Loaded {len(test_places)} places")
    if test_flights:
        print(f"Sample flight: {test_flights[0]}")
    if test_places:
        print(f"Sample place: {test_places[0]}")
except Exception as e:
    print(f"✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
print("=" * 60)

# Page configuration
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #1565C0;
    }
    </style>
""", unsafe_allow_html=True)


def create_agent():
    """Create the travel planning agent."""
    
    # Initialize LLM
    llm = ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model_name=settings.GROQ_MODEL,
        temperature=settings.MODEL_TEMPERATURE,
        max_tokens=settings.MAX_TOKENS
    )
    
    # Initialize tools
    tools = [
        FlightSearchTool(),
        HotelRecommendationTool(),
        PlacesDiscoveryTool(),
        WeatherLookupTool(),
        BudgetEstimationTool()
    ]
    
    # Create prompt
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
    
    # Create agent
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    
    # Create executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=15,
        handle_parsing_errors=True,
        return_intermediate_steps=True
    )
    
    return agent_executor


def initialize_session_state():
    """Initialize session state variables."""
    if 'agent' not in st.session_state:
        st.session_state.agent = None
    if 'result' not in st.session_state:
        st.session_state.result = None
    if 'show_intermediate' not in st.session_state:
        st.session_state.show_intermediate = False


def load_data_options():
    """Load options for dropdowns from data files."""
    try:
        flights = DataLoader.load_json(settings.FLIGHTS_PATH)
        places = DataLoader.load_json(settings.PLACES_PATH)
        
        print(f"DEBUG: Loaded {len(flights)} flights")
        print(f"DEBUG: Loaded {len(places)} places")
        
        # Use 'from' and 'to' fields from your data
        cities = sorted(list(set(
            [f.get('from') for f in flights if f.get('from')] +
            [f.get('to') for f in flights if f.get('to')]
        )))
        
        # Use 'type' field from your data
        categories = sorted(list(set(
            [p.get('type') for p in places if p.get('type')]
        )))
        
        print(f"DEBUG: Found {len(cities)} cities")
        print(f"DEBUG: Found {len(categories)} categories")
        print(f"DEBUG: Cities: {cities}")
        print(f"DEBUG: Categories: {categories}")
        
        return cities, categories
    except Exception as e:
        st.error(f"Error loading data: {e}")
        import traceback
        st.code(traceback.format_exc())
        print(f"ERROR in load_data_options: {e}")
        print(traceback.format_exc())
        return [], []


def render_header():
    """Render the application header."""
    st.markdown('<h1 class="main-header">✈️ AI Travel Planning Assistant</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Let AI plan your perfect trip with personalized itineraries, '
        'real-time weather, and budget optimization</p>',
        unsafe_allow_html=True
    )


def render_sidebar():
    """Render the sidebar."""
    with st.sidebar:
        st.markdown("## 📋 About")
        st.info(
            "This intelligent travel assistant uses LangChain and Groq's LLM "
            "to create personalized trip itineraries."
        )
        
        st.markdown("## 🎯 Features")
        st.markdown("""
        - 🔍 Smart flight search
        - 🏨 Hotel recommendations
        - 📍 Places discovery
        - 🌤️ Real-time weather
        - 💰 Budget calculation
        - 📅 Day-wise itinerary
        """)
        
        st.markdown("## 🛠️ Tech Stack")
        st.markdown("""
        - **LLM**: Groq (Llama 3.3)
        - **Framework**: LangChain
        - **UI**: Streamlit
        """)
        
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        show_reasoning = st.checkbox("Show AI Reasoning", value=False)
        st.session_state.show_intermediate = show_reasoning
        
        if st.button("🔄 Reset"):
            st.session_state.clear()
            st.rerun()


def render_input_form(cities, categories):
    """Render input form."""
    st.markdown("## 🗺️ Plan Your Trip")
    
    col1, col2 = st.columns(2)
    
    with col1:
        source = st.selectbox(
            "📍 Source City",
            options=cities,
            index=cities.index("Delhi") if "Delhi" in cities else 0
        )
        
        start_date = st.date_input(
            "📅 Start Date",
            value=datetime.now() + timedelta(days=7),
            min_value=datetime.now()
        )
        
        budget = st.number_input(
            "💰 Total Budget (₹)",
            min_value=5000,
            max_value=500000,
            value=30000,
            step=5000
        )
    
    with col2:
        destination = st.selectbox(
            "🎯 Destination City",
            options=cities,
            index=cities.index("Goa") if "Goa" in cities else 1
        )
        
        num_days = st.slider(
            "📆 Number of Days",
            min_value=3,
            max_value=7,
            value=5
        )
    
    st.markdown("### 🎨 Preferences")
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        flight_pref = st.radio(
            "✈️ Flight Preference",
            options=["Cheapest", "Fastest"]
        )
    
    with col4:
        hotel_rating = st.select_slider(
            "🏨 Hotel Rating",
            options=[3.0, 3.5, 4.0, 4.5, 5.0],
            value=4.0
        )
    
    with col5:
        interests = st.multiselect(
            "🎭 Interests",
            options=categories,
            default=[categories[0]] if categories else []
        )
    
    return {
        "source": source,
        "destination": destination,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "num_days": num_days,
        "budget": budget,
        "preferences": {
            "flight_preference": flight_pref.lower(),
            "hotel_rating": hotel_rating,
            "interests": interests
        }
    }


def build_query(source, destination, start_date, num_days, budget, preferences):
    """Build query for the agent."""
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


def render_results(result: Dict[str, Any]):
    """Render results."""
    if not result.get("success"):
        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        return
    
    st.markdown("## 🎉 Your Trip Itinerary")
    
    itinerary = result.get("itinerary", "")
    
    if itinerary:
        st.markdown("### 📋 Complete Itinerary")
        st.markdown(itinerary)
        
        st.download_button(
            label="📥 Download Itinerary",
            data=itinerary,
            file_name=f"trip_itinerary_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
    
    if st.session_state.show_intermediate:
        st.markdown("---")
        st.markdown("### 🔍 AI Reasoning Process")
        
        intermediate_steps = result.get("intermediate_steps", [])
        
        if intermediate_steps:
            for i, step in enumerate(intermediate_steps, 1):
                with st.expander(f"Step {i}"):
                    st.write("**Action:**", step[0].tool if hasattr(step[0], 'tool') else "N/A")
                    st.write("**Input:**", step[0].tool_input if hasattr(step[0], 'tool_input') else "N/A")
                    st.write("**Output:**", step[1] if len(step) > 1 else "N/A")


def main():
    """Main application."""
    initialize_session_state()
    render_header()
    render_sidebar()
    
    # Load data
    cities, categories = load_data_options()
    
    if not cities or not categories:
        st.error("""
        ⚠️ **Data files not found!**
        
        Please ensure these files exist in the `data/` folder:
        - flights.json
        - hotels.json
        - places.json
        """)
        return
    
    # Input form
    inputs = render_input_form(cities, categories)
    
    # Plan button
    st.markdown("---")
    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        plan_button = st.button("🚀 Plan My Trip", use_container_width=True)
    
    if plan_button:
        if inputs["source"] == inputs["destination"]:
            st.warning("⚠️ Source and destination cannot be the same!")
            return
        
        with st.spinner("🤖 AI is planning your perfect trip..."):
            try:
                # Create agent if needed
                if st.session_state.agent is None:
                    st.session_state.agent = create_agent()
                
                # Build query
                query = build_query(
                    inputs["source"],
                    inputs["destination"],
                    inputs["start_date"],
                    inputs["num_days"],
                    inputs["budget"],
                    inputs["preferences"]
                )
                
                # Execute
                result = st.session_state.agent.invoke({
                    "input": query,
                    "chat_history": ""
                })
                
                st.session_state.result = {
                    "success": True,
                    "itinerary": result.get("output", ""),
                    "intermediate_steps": result.get("intermediate_steps", [])
                }
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.result = {
                    "success": False,
                    "error": str(e)
                }
    
    # Display results
    if st.session_state.result:
        render_results(st.session_state.result)


if __name__ == "__main__":
    main()