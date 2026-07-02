from pydantic import BaseModel


class WeatherCurrent(BaseModel):
    city: str
    country: str
    temperature: float
    feels_like: float
    humidity: float
    wind_speed: float
    description: str
    icon: str


class WeatherForecast(BaseModel):
    date: str
    temp_min: float
    temp_max: float
    description: str
    icon: str