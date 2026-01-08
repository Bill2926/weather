import json
from pathlib import Path

wmo_codes_path = Path(__file__).parent.parent /'external_data'/'wmo_weather_codes.json'

class DayForecastWeather:
    def __init__(self, timestamp, description, temp_min, temp_max):
        self.timestamp = timestamp
        self.description = description
        self.temp_min = temp_min
        self.temp_max = temp_max
    
    def __repr__(self):  # Add this to print the object nicely
        return f"DayForecastWeather(timestamp='{self.timestamp}', description='{self.description}', temp_min={self.temp_min}, temp_max={self.temp_max})"

    def display_day_forecast_weather(self):
        """Display formatted daily forecast weather information"""
        print(f"📅 Date: {self.timestamp}")
        print(f"🌡️  Temperature: {self.temp_min}°C - {self.temp_max}°C")
        print(f"☁️  Condition: {self.description}")
        print("-" * 50)

    @classmethod
    def from_dict(cls, weather_dict):
        weather_code = str(weather_dict['weather_code'])  # ← Convert to string!
        with open(wmo_codes_path, "r", encoding="utf-8") as f:
            wmo_codes_data = json.load(f)
            if weather_code in wmo_codes_data["weather_codes"]:
                weather_description = wmo_codes_data["weather_codes"][weather_code]["description"]
            else:
                print(f"Warning: Weather code '{weather_code}' not found")
                weather_description = "Unknown weather"
        return cls(
            timestamp=weather_dict['time_stamp'],
            description=weather_description,
            temp_min=weather_dict['temp_min'],
            temp_max=weather_dict['temp_max'],
        )