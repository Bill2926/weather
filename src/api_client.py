import requests
import asyncio
from datetime import datetime
from config import Config

class API_Client:
    def __init__(self, base_url, daily_url, geocoding_url, api_key):
        self.base_url = base_url
        self.daily_url = daily_url
        self.geocoding_url = geocoding_url
        self.api_key = api_key
        self.current_date = datetime.now()

    def get_current_weather(self, city_code):
        url = f"{self.base_url}/weather?id={city_code}&appid={self.api_key}&units=metric"
        # send a GET method to the destination url
        response = requests.get(url)
        if response.status_code == 200:
            asyncio.run(self._simulate_delay())
            response_dict = response.json()  # This returns a dictionary
            return self._parse_current_dict(response_dict)
        else:
            print('There must be a problem.')
    
    def get_geocoding(self, city_name):
        url = f"{self.geocoding_url}/direct?q={city_name}&appid={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            response_dict = response.json()  # This returns a dictionary
            
            if len(response_dict) == 0:
                return False
            elif len(response_dict) == 1:
                x = response_dict[0]
                coord = (x['lat'], x['lon'])
                return coord
            else:
                result_list = []
                for i in response_dict:
                    result_list.append({
                        "city_name": i["name"],
                        "country": i["country"],
                        "lat": i["lat"],
                        "lon": i["lon"]
                    })
                
                for r in result_list:
                    i = 1
                    print(f"{i}. {r['city_name']} / {r['country']}")
                    i += 1

                print('Please choose your prefered city:')
                choice = int(input("> "))
                if choice:
                    selected = result_list[choice-1]
                    coord = (selected['lat'], selected['lon'])
                    return coord
        else:
            print('There must be a problem.')
    
    def get_day_forecast(self, coord, days):
        """
        This function will use Meteo API
        Using lat and longtitude numbers instead
        """
        lat, lon = coord
        url = f"{self.daily_url}latitude={lat}&longitude={lon}&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto&forecast_days={days}"
        response = requests.get(url)
        if response.status_code == 200:
            # Later on add the delay
            response_dict = response.json()
            # return self._parse_day_dict(response_dict)
            return self._parse_day_dict(response_dict)
        else:
            print('There must be a problem.')

    def _parse_current_dict(self, response_dict):
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

    def _parse_day_dict(self, response_dict):
        data = response_dict["daily"]
        time_stamps = data["time"]
        weather_code = data["weather_code"]
        temp_max = data["temperature_2m_max"]
        temp_min = data["temperature_2m_min"]
        forecast_weather_data_list = []

        x = zip(time_stamps, weather_code, temp_min, temp_max)
        for tuple in x:
            forecast_day = {
                "time_stamp": tuple[0],
                "weather_code": tuple[1],
                "temp_min": tuple[2],
                "temp_max": tuple[3]
            }
            forecast_weather_data_list.append(forecast_day)
        
        return forecast_weather_data_list

    async def _simulate_delay(self):
        print('Fetching data, please wait... 🔍')
        await asyncio.sleep(1.5)
        print('Fetched Successfully ✅')


# config = Config.load()
# api = API_Client(config.base_url, config.daily_url, config.geocoding_url, config.api_key)
# coord = api.get_geocoding("1581130")
# # coord = api.get_geocoding("18093")
# list = api.get_day_forecast(coord, "3")

# print(list)
# print(coord)