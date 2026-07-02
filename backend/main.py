from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.weather import fetch_weather_data

app = FastAPI(title="Responsive Weather API")

app.add_middleware(
    CORSMiddleware,
    allow_origins =["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/weather/{city}")
async def get_req_city(city: str):
    result = await fetch_weather_data(city)

    if result is None:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found or API error occured")
    return result