# 🌍 AI-Powered Travel Planning Assistant

An intelligent, agentic AI system built with LangChain and Groq that autonomously creates personalized trip itineraries with real-time weather data, flight options, hotel recommendations, and tourist attractions.

## 🚀 Features

- **Intelligent Agent System**: Uses LangChain ReAct agents with Groq's LLM for autonomous decision-making
- **Multi-Tool Integration**: 
  - Flight search and comparison
  - Hotel recommendations with ratings
  - Places of interest discovery
  - Real-time weather forecasts
  - Automatic budget estimation
- **Smart Reasoning**: Agent explains its decisions and recommendations
- **Interactive UI**: Beautiful Streamlit interface with real-time updates
- **Structured Output**: Day-wise itineraries with complete travel information

## 📋 Prerequisites

- Python 3.8+
- Anaconda (recommended)
- Groq API Key (free at https://console.groq.com)

## 🛠️ Installation

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd ai-travel-planner
```

### Step 2: Create Conda Environment

```bash
conda create -n travel-ai python=3.10
conda activate travel-ai
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

### Step 5: Download Data Files

Download the JSON datasets from the provided Google Drive link and place them in the `data/` folder:
- flights.json
- hotels.json
- places.json

## 🎯 Usage

### Run the Streamlit Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Using the Application

1. **Enter Travel Details**:
   - Source city
   - Destination city
   - Start date
   - Number of days (3-7)
   - Budget constraints

2. **Customize Preferences**:
   - Hotel rating preference
   - Flight priority (cheapest/fastest)
   - Interest categories (beaches, heritage, adventure, etc.)

3. **Generate Itinerary**:
   - Click "Plan My Trip"
   - Watch the AI agent work through its reasoning
   - Get a complete itinerary with all details

## 🏗️ Project Architecture

### Directory Structure
```
ai-travel-planner/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── config/
│   └── settings.py
├── data/
│   ├── flights.json
│   ├── hotels.json
│   └── places.json
├── src/
│   ├── __init__.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── flight_tool.py
│   │   ├── hotel_tool.py
│   │   ├── places_tool.py
│   │   ├── weather_tool.py
│   │   └── budget_tool.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── travel_agent.py
│   └── utils/
│       ├── __init__.py
│       └── data_loader.py
├── app.py
└── tests/
    └── __init__.py
```

## 📊 Sample Output

```
Your 5-Day Trip to Goa (Feb 15–19, 2025)

Flight Selected:
✈️ IndiGo (₹4,800) – Departs Delhi at 14:00, Duration: 2.5 hours

Hotel Booked:
🏨 Sea View Resort (₹3,200/night, 4.5⭐)
   Amenities: WiFi, Pool, Beach Access

Weather Forecast:
☀️ Day 1: Sunny (31°C)
⛅ Day 2: Partly Cloudy (29°C)
☀️ Day 3: Clear Sky (32°C)
🌤️ Day 4: Light Breeze (30°C)
⛅ Day 5: Partly Cloudy (28°C)

Day-wise Itinerary:

Day 1 - Arrival & Beach Time
• Baga Beach (4.7⭐) - Popular beach destination
• Candolim Market - Evening shopping

Day 2 - Heritage Tour
• Basilica of Bom Jesus (4.8⭐) - UNESCO World Heritage Site
• Old Goa Heritage Walk

Day 3 - Adventure Day
• Water Sports at Calangute Beach
• Parasailing and Jet Skiing

Day 4 - Culture & Cuisine
• Spice Plantation Tour
• Local Goan Cuisine Experience

Day 5 - Relaxation & Departure
• Morning at Anjuna Beach
• Departure preparations

Budget Breakdown:
💰 Flight: ₹4,800
🏨 Hotel (4 nights): ₹12,800
🍽️ Food & Local Travel: ₹10,000
━━━━━━━━━━━━━━━━━━━━━━━━
💵 Total Cost: ₹27,600
```

## 🎨 Key Features That Impress

### 1. **Agentic Reasoning**
- Agent explains why it chose specific flights, hotels, and attractions
- Transparent decision-making process visible to users

### 2. **Real-Time Data Integration**
- Live weather forecasts for travel dates
- Dynamic budget calculations

### 3. **Smart Optimization**
- Balances price, quality, and user preferences
- Considers travel distances and time management

### 4. **Professional Code Quality**
- PEP 8 compliant
- Comprehensive error handling
- Modular, reusable components
- Extensive documentation

### 5. **Production-Ready**
- Environment variable management
- Logging and monitoring
- Scalable architecture
- Unit test structure

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v
```

## 📈 Future Enhancements

- [ ] Database integration for user history
- [ ] Multi-city trip support
- [ ] Collaborative trip planning
- [ ] Integration with booking APIs
- [ ] Mobile app version
- [ ] User reviews and ratings
- [ ] AI-powered photo recommendations

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Created as part of an AI/ML capstone project demonstrating:
- Advanced LangChain agent development
- Groq LLM integration
- Production-ready Python application design
- Modern UI/UX with Streamlit

## 🙏 Acknowledgments

- LangChain for the agent framework
- Groq for fast LLM inference
- Open-Meteo for free weather API
- Streamlit for rapid UI development

---

**Built with ❤️ using LangChain, Groq, and Streamlit**