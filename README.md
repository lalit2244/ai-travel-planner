# ✈️ AI-Powered Travel Planning Assistant

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-travel-planner-khwdtrlneyutchs3gvblef.streamlit.app)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An intelligent, agentic AI system built with LangChain and Groq that autonomously creates personalized trip itineraries with real-time weather data, flight options, hotel recommendations, and tourist attractions.

## 🌐 Live Demo

**[Try the App Live →](https://ai-travel-planner-khwdtrlneyutchs3gvblef.streamlit.app)**

---

## 🎥 Demo

![AI Travel Planner Demo](https://img.shields.io/badge/Status-Live-success)

**Key Features in Action:**
- 🤖 AI Agent autonomously plans your entire trip
- ✈️ Smart flight search with price comparison
- 🏨 Hotel recommendations based on preferences
- 📍 Curated places to visit
- 🌤️ Real-time weather forecasts
- 💰 Complete budget breakdown
- 💬 Natural language query support

---

## 🚀 Features

### 🧠 Intelligent AI Agent
- **Autonomous Decision Making**: ReAct agent decides which tools to use and when
- **Multi-Step Reasoning**: Breaks complex planning into logical steps
- **Transparent Process**: See exactly how the AI thinks and makes decisions

### 🛠️ Multi-Tool Integration
Five specialized tools working together:
- **Flight Search Tool**: Filters by price, duration, and route
- **Hotel Recommendation Tool**: Considers rating, price, and amenities
- **Places Discovery Tool**: Finds attractions by category and rating
- **Weather Lookup Tool**: Real-time 7-day forecasts via Open-Meteo API
- **Budget Estimation Tool**: Complete cost breakdown with daily expenses

### 💬 Natural Language Queries
Ask in plain English:
- _"Plan a romantic 5-day beach vacation to Goa under ₹30,000"_
- _"I want to visit historical places in Delhi for 3 days with luxury hotels"_
- _"Budget trip to Bangalore for 4 days, interested in nature and food"_

### 📊 Smart Optimization
- Balances multiple constraints (budget, quality, preferences)
- Considers geographical distances
- Optimizes day-wise scheduling
- Provides reasoning for recommendations

---

## 🏗️ Architecture

```
┌─────────────────┐
│   User Input    │
│  (Streamlit UI) │
└────────┬────────┘
         │
         ▼
┌────────────────────────┐
│   Travel Agent         │
│   (LangChain ReAct)    │
│   + Groq LLM           │
└───────┬────────────────┘
        │
        ├──────────┬──────────┬──────────┬──────────┐
        │          │          │          │          │
        ▼          ▼          ▼          ▼          ▼
    ┌──────┐  ┌───────┐  ┌───────┐  ┌────────┐  ┌────────┐
    │Flight│  │Hotel  │  │Places │  │Weather │  │Budget  │
    │Tool  │  │Tool   │  │Tool   │  │Tool    │  │Tool    │
    └───┬──┘  └───┬───┘  └───┬───┘  └───┬────┘  └───┬────┘
        │         │          │          │           │
        ▼         ▼          ▼          ▼           ▼
    ┌──────────────────────────────────────────────────┐
    │             Data Sources                          │
    │  • flights.json  • hotels.json  • places.json    │
    │  • Open-Meteo API (Real-time Weather)            │
    └──────────────────────────────────────────────────┘
```

---

## 💻 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | Groq (Llama 3.3 70B) | Fast, intelligent decision-making |
| **Framework** | LangChain | Agent orchestration and tool management |
| **UI** | Streamlit | Interactive web interface |
| **Language** | Python 3.11 | Core development |
| **Weather API** | Open-Meteo | Real-time weather forecasts (free) |
| **Data Format** | JSON | Data storage and exchange |

### Why These Technologies?

**Groq over OpenAI:**
- ✅ Free tier with generous limits
- ✅ Extremely fast inference (400+ tokens/sec)
- ✅ Excellent at reasoning tasks
- ✅ No billing/credit card required

**LangChain:**
- ✅ Industry-standard for agentic AI
- ✅ ReAct agent pattern for transparent reasoning
- ✅ Easy tool integration
- ✅ Extensible architecture

---

## 📋 Installation

### Prerequisites
- Python 3.11+
- pip or conda
- Groq API Key (free from [console.groq.com](https://console.groq.com))

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/lalit2244/ai-travel-planner.git
cd ai-travel-planner
```

2. **Create virtual environment**
```bash
# Using conda
conda create -n travel-ai python=3.11
conda activate travel-ai

# Or using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your Groq API key
GROQ_API_KEY=your_groq_api_key_here
```

5. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🎯 Usage

### Structured Form Input
1. Select source and destination cities
2. Choose travel dates and duration
3. Set your budget
4. Select preferences (flight type, hotel rating, interests)
5. Click "Plan My Trip"

### Natural Language Input
Simply describe your ideal trip:
```
"Plan a 5-day family trip to Goa starting next week. 
We love beaches and want good hotels around ₹3000 per night. 
Total budget is ₹40,000."
```

### Example Queries
- 🏖️ Romantic beach getaway to Goa for 5 days under ₹35,000
- 🏛️ Weekend trip to Jaipur for heritage exploration
- 👨‍👩‍👧‍👦 Family vacation to Bangalore with kids, 4 days, budget ₹50,000
- 💎 Luxury 3-day trip to Mumbai with 5-star hotels
- 🎒 Budget backpacking trip to Delhi for 6 days

---

## 📊 Sample Output

```
Your 5-Day Trip to Goa (Feb 15–19, 2025)

Flight Selected:
✈️ IndiGo (₹4,800) – Departs Delhi at 14:00, Duration: 2.5 hours

Hotel Booked:
🏨 Royal Heritage (₹2,828/night, 5⭐)
   Amenities: WiFi, Pool, Beach Access, Restaurant, Spa

Weather Forecast:
☀️ Day 1: Sunny (31°C)
⛅ Day 2: Partly Cloudy (29°C)
☀️ Day 3: Clear Sky (32°C)
🌤️ Day 4: Light Breeze (30°C)
⛅ Day 5: Partly Cloudy (28°C)

Day-wise Itinerary:

Day 1 - Arrival & Beach Time
• Famous Park (Museum, 4.5⭐) - Cultural exploration
• Beautiful Park (Fort, 4.3⭐) - Historical site visit

Day 2 - Heritage Tour
• Popular Lake (Museum, 4.2⭐) - Scenic beauty
• Historic Park (Fort, 4.1⭐) - Heritage walk

Day 3 - Adventure Day
• Beach activities and water sports
• Local market exploration

Day 4 - Culture & Cuisine
• Beautiful Lake (Market, 4.0⭐)
• Local Goan cuisine experience

Day 5 - Relaxation & Departure
• Morning leisure time
• Departure preparations

Budget Breakdown:
💰 Flight: ₹4,800
🏨 Hotel (4 nights): ₹11,312
🍽️ Food & Local Travel: ₹10,000
━━━━━━━━━━━━━━━━━━━━━━━━
💵 Total Cost: ₹26,112
```

---

## 📁 Project Structure

```
ai-travel-planner/
├── README.md                      # Project documentation
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── .python-version               # Python version specification
├── app.py                        # Main Streamlit application
│
├── config/
│   └── settings.py               # Configuration management
│
├── data/
│   ├── flights.json              # Flight data (30 records)
│   ├── hotels.json               # Hotel data (40 records)
│   └── places.json               # Places data (40 records)
│
├── src/
│   ├── __init__.py
│   ├── tools/                    # LangChain tools
│   │   ├── __init__.py
│   │   ├── flight_tool.py        # Flight search functionality
│   │   ├── hotel_tool.py         # Hotel recommendations
│   │   ├── places_tool.py        # Places discovery
│   │   ├── weather_tool.py       # Weather forecasts
│   │   └── budget_tool.py        # Budget calculations
│   ├── agents/                   # Agent implementations
│   │   ├── __init__.py
│   │   └── travel_agent.py       # Main ReAct agent
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       └── data_loader.py        # Data loading with caching
│
└── tests/                        # Unit tests
    ├── __init__.py
    └── test_tools.py
```

---

## 🎨 Key Features That Impress

### 1. **Agentic Reasoning**
- Agent explains why it chose specific flights, hotels, and attractions
- Transparent decision-making process visible to users
- Multi-step thinking with clear logical flow

### 2. **Real-Time Data Integration**
- Live weather forecasts for travel dates
- Dynamic budget calculations
- Up-to-date place ratings and prices

### 3. **Smart Optimization**
- Balances price, quality, and user preferences
- Considers travel distances and time management
- Provides reasoning for each recommendation

### 4. **Professional Code Quality**
- PEP 8 compliant
- Comprehensive error handling
- Modular, reusable components
- Extensive documentation
- Type hints throughout

### 5. **Production-Ready**
- Environment variable management
- Logging and monitoring
- Scalable architecture
- Unit test structure
- CI/CD ready

---

## 🔧 Configuration

Edit `config/settings.py` to customize:
- LLM model selection
- Temperature and creativity settings
- Default budget parameters
- City coordinates for weather
- Cache settings

Or use environment variables in `.env`:
```bash
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
MODEL_TEMPERATURE=0.3
MAX_TOKENS=4096
DEFAULT_DAILY_EXPENSE=2000
```

---

## 🧪 Testing

Run tests:
```bash
pytest tests/ -v
```

Test individual components:
```bash
# Test configuration
python config/settings.py

# Test data loader
python src/utils/data_loader.py

# Test specific tool
python src/tools/flight_tool.py
```

---

## 🚀 Deployment

### Deployed on Streamlit Community Cloud

**Live URL**: [https://ai-travel-planner-khwdtrlneyutchs3gvblef.streamlit.app](https://ai-travel-planner-khwdtrlneyutchs3gvblef.streamlit.app)

### Deploy Your Own

1. Fork this repository
2. Sign up at [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add secrets (GROQ_API_KEY)
5. Deploy!

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed deployment instructions.

---

## 📈 Future Enhancements

- [ ] Database integration for user history
- [ ] Multi-city trip support
- [ ] Collaborative trip planning
- [ ] Integration with booking APIs (MakeMyTrip, Booking.com)
- [ ] Mobile app version
- [ ] User reviews and ratings system
- [ ] AI-powered photo recommendations
- [ ] Export to PDF/Calendar
- [ ] Multi-language support
- [ ] Currency conversion
- [ ] Visa requirement checking
- [ ] Travel insurance suggestions

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code follows PEP 8 standards and includes appropriate tests.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Lalit Kumar**

- GitHub: [@lalit2244](https://github.com/lalit2244)
- Project Link: [https://github.com/lalit2244/ai-travel-planner](https://github.com/lalit2244/ai-travel-planner)
- Live Demo: [https://ai-travel-planner-khwdtrlneyutchs3gvblef.streamlit.app](https://ai-travel-planner-khwdtrlneyutchs3gvblef.streamlit.app)

---

## 🙏 Acknowledgments

- **LangChain** - For the powerful agent framework
- **Groq** - For lightning-fast LLM inference
- **Streamlit** - For the amazing web framework
- **Open-Meteo** - For free weather API
- **Anthropic** - For inspiration in agent design patterns

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/lalit2244/ai-travel-planner/issues) page
2. Open a new issue with detailed description
3. Contact via GitHub discussions

---

## ⭐ Show Your Support

If you find this project useful, please consider:
- Giving it a ⭐ on GitHub
- Sharing it with others
- Contributing to the codebase
- Reporting bugs or suggesting features

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/lalit2244/ai-travel-planner?style=social)
![GitHub forks](https://img.shields.io/github/forks/lalit2244/ai-travel-planner?style=social)
![GitHub issues](https://img.shields.io/github/issues/lalit2244/ai-travel-planner)
![GitHub pull requests](https://img.shields.io/github/issues-pr/lalit2244/ai-travel-planner)

---

<div align="center">

**Built with ❤️ using LangChain, Groq, and Streamlit**

[🌐 Live Demo](https://ai-travel-planner-khwdtrlneyutchs3gvblef.streamlit.app) • [📖 Documentation](https://github.com/lalit2244/ai-travel-planner) • [🐛 Report Bug](https://github.com/lalit2244/ai-travel-planner/issues) • [✨ Request Feature](https://github.com/lalit2244/ai-travel-planner/issues)

</div>
