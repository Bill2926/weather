class Weather:
    def __init__(self, temperature, feel, temp_min, temp_max, wind_speed, humidity, description):
        self.temperature = temperature
        self.feel = feel
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.wind_speed = wind_speed
        self.humidity = humidity
        self.description = description
    
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