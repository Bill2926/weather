from api_client import API_Client
from config import Config
from weather import Weather
from city import City, find_by_city_name

# Initialization
config = Config.load()
api_client = API_Client(config.base_url, config.api_key)

def main():
    print('WEATHER API v1.0')
    print('Enter your city:')
    input_city = input('> ')

    if input_city:
        city_code = find_by_city_name(input_city)
        result = api_client.get_current_weather(city_code)

        city_dict, weather_dict = result # unpacking
        city = City.from_dict(city_dict)
        weather = Weather.from_dict(weather_dict)

        weather.display_weather()
        city.display_city()
    else: 
        print('There must be something wrong.')



if __name__ == "__main__":
    main()