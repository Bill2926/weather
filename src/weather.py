class Weather:
    def __init__(self, temperature, feel, temp_min, temp_max, wind_speed, humidity, description):
        self.temperature = temperature
        self.feel = feel
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.wind_speed = wind_speed
        self.humidity = humidity
        self.description = description
    
    def display_weather(self):
        # Weather icon based on description
        weather_icon = self._get_weather_icon()
        
        print("\n" + "=" * 50)
        print(f"WEATHER REPORT")
        print("=" * 50)
        print(f"Description:   {self.description.capitalize()} {weather_icon}")
        print(f"Temperature:   {self.temperature}°C")
        print(f"Feels Like:    {self.feel}°C")
        print(f"Min/Max:       {self.temp_min}°C / {self.temp_max}°C")
        print("-" * 40)
        print(f"💨 Wind Speed:  {self.wind_speed} m/s")
        print(f"💧 Humidity:    {self.humidity}%")
        print("-" * 40 + "\n")
    
    def _get_weather_icon(self):
        description_lower = self.description.lower()
        if 'clear' in description_lower:
            return '☀️'
        elif 'cloud' in description_lower:
            return '☁️'
        elif 'rain' in description_lower:
            return '🌧️'
        elif 'storm' in description_lower or 'thunder' in description_lower:
            return '⛈️'
        elif 'snow' in description_lower:
            return '❄️'
        elif 'mist' in description_lower or 'fog' in description_lower:
            return '🌫️'
        else:
            return '🌤️'

    @classmethod
    def from_dict(cls, weather_dict):
        """Create Weather instance from dictionary"""
        return cls(
            temperature=weather_dict['temperature'],
            feel=weather_dict['feel'], 
            temp_min=weather_dict['temp_min'],
            temp_max=weather_dict['temp_max'],
            wind_speed=weather_dict['wind_speed'],
            humidity=weather_dict['humidity'],
            description=weather_dict['description']
        )   