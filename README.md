# Eco-Weather Microservice

A sustainable weather microservice that provides weather data and environmental impact insights.

## Features

- Fetch real-time weather data for any city
- Calculate approximate carbon impact of temperature regulation
- Implement efficient caching to reduce API calls and energy usage
- Async operations for better resource utilization

## Prerequisites

- Python 3.8+
- Redis
- OpenWeatherMap API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/TuomoVVP/COMP.SE.221
cd COMP.SE.221
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install fastapi uvicorn httpx redis python-dotenv
```

4. Create .env file:
```
OPENWEATHER_API_KEY=your_api_key_here
```

## Running the Service

```bash
uvicorn main:app --reload
```

Access the API documentation at `http://localhost:8000/docs`

## API Endpoints

- GET `/weather/{city}`: Get weather data and carbon impact for a city

## Sustainability Features

1. **Efficient Caching**: Reduces API calls and server load
2. **Async Operations**: Optimizes resource usage
3. **Carbon Impact Calculation**: Raises awareness about environmental impact
