import requests
import asyncio
from datetime import datetime
# from config import Config

class API_Client:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.current_date = datetime.now()

    def get_current_weather(self, city_code):
        url = f"{self.base_url}/weather?id={city_code}&appid={self.api_key}&units=metric"
        # send a GET method to the destination url
        response = requests.get(url)
        if response.status_code == 200:
            asyncio.run(self._simulate_delay())
            response_dict = response.json()  # This returns a dictionary
            return self._parse_temp_dict(response_dict)
        else:
            print('There must be a problem.')

    def _parse_temp_dict(self, response_dict):
        # city = response_dict['name']
        city_dict = {
            'city_id': response_dict['id'],
            'city_name': response_dict['name'],
            'city_country': response_dict['sys']['country'],
            'city_lat': response_dict['coord']['lat'],
            'city_lon': response_dict['coord']['lon']
        }

        main = response_dict['main']
        weather = response_dict['weather'][0] # weather is a list
        wind = response_dict['wind']
        weather_dict = {
            'temperature': main['temp'],
            'feel': main['feels_like'],
            'temp_min': main['temp_min'],
            'temp_max': main['temp_max'],
            'wind_speed': wind['speed'],
            'humidity': main['humidity'],
            'description': weather['main']
        }

        result_list = [city_dict, weather_dict]
        return result_list

    async def _simulate_delay(self):
        print('Fetching data, please wait... 🔍')
        await asyncio.sleep(1.5)
        print('Fetched Successfully ✅')