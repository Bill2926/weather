from api_client import API_Client
from config import Config
from weather import Weather
from city import City

# Initialization
config = Config.load()
api_client = API_Client(config.base_url, config.api_key)
sydney = '2147714'

result = api_client.get_current_weather(sydney)
city_dict, weather_dict = result # unpacking
city = City.from_dict(city_dict)
weather = Weather.from_dict(weather_dict)
print(city.name)
print('')
for key, value in weather_dict.items():
        print(f"{key}: {value}")