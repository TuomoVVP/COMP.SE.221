# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import httpx
from datetime import datetime
import redis
import os
from dotenv import load_load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Eco-Weather Service")
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    humidity: int
    wind_speed: float
    carbon_impact: float
    timestamp: str

@app.get("/weather/{city}", response_model=WeatherResponse)
async def get_weather(city: str):
    # Check cache first
    cached_data = redis_client.get(city)
    if cached_data:
        return WeatherResponse.parse_raw(cached_data)
    
    # If not in cache, fetch from OpenWeatherMap
    api_key = os.getenv("OPENWEATHER_API_KEY")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="City not found")
        
        data = response.json()
        
        # Calculate approximate carbon impact based on temperature and HVAC usage
        temp = data['main']['temp']
        carbon_impact = abs(temp - 20) * 0.1  # Rough estimate of kg CO2 per degree from optimal
        
        weather_data = WeatherResponse(
            city=city,
            temperature=temp,
            humidity=data['main']['humidity'],
            wind_speed=data['wind']['speed'],
            carbon_impact=carbon_impact,
            timestamp=datetime.now().isoformat()
        )
        
        # Cache for 30 minutes
        redis_client.setex(city, 1800, weather_data.json())
        
        return weather_data

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)