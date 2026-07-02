import os
import httpx
import asyncio
from dotenv import load_dotenv
from models.schemas import WeatherCurrent, WeatherForecast

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY") or ""
BASE_URL = "https://api.openweathermap.org/data/2.5"

async def fetch_weather_data(city: str, api_key: str = API_KEY):
    async with httpx.AsyncClient() as client:
        # Stage 1: Fetching the data concurrently
        response_current = client.get(url=f"{BASE_URL}/weather", params={"q": city, "appid": api_key, "units": "metric"})
        response_forecast = client.get(url=f"{BASE_URL}/forecast", params={"q": city, "appid": api_key, "units": "metric"})
        
        current, forecast = await asyncio.gather(response_current, response_forecast)
        
        # Stage 2: Handling 404 errors
        if current.status_code == 404 or forecast.status_code == 404:
            return None
            
        # Stage 3: Building the WeatherCurrent object
        current_data = current.json()
        
        current_weather = WeatherCurrent(
            city=current_data["name"],
            country=current_data["sys"]["country"],
            temperature=current_data["main"]["temp"],
            feels_like=current_data["main"]["feels_like"],
            humidity=current_data["main"]["humidity"],
            wind_speed=current_data["wind"]["speed"],
            description=current_data["weather"][0]["description"],
            icon=current_data["weather"][0]["icon"]
        )
        
        # Stage 4: Building the forecast list
        forecast_data = forecast.json()
        forecast_list = forecast_data["list"]
        daily_forecasts = []

        for entry in forecast_list:
            if "12:00:00" in entry["dt_txt"]:
                forecast_weather = WeatherForecast(
                    date=entry["dt_txt"],
                    temp_min=entry["main"]["temp_min"],
                    temp_max=entry["main"]["temp_max"],
                    description=entry["weather"][0]["description"],
                    icon=entry["weather"][0]["icon"]
                )
                daily_forecasts.append(forecast_weather)
                
        # Stage 5: Return the data
        return current_weather, daily_forecasts