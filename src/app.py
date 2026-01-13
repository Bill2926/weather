# This file hosts Flask framework to deploy
from flask import Flask, jsonify, request, render_template
from api_client import API_Client
from config import Config
from weather import Weather
from city import City, find_by_city_name, find_by_city_code
from day_forecast_weather import DayForecastWeather

# Initialization
config = Config.load()
api_client = API_Client(config.base_url, config.daily_url, config.geocoding_url, config.api_key)
app = Flask(__name__)   # Create Flask app instance

@app.route("/") # Create route to the main page
def index():
    return render_template("index.html")

@app.route("/api/current-weather", methods=["GET"])
def get_current_weather():
    # Parse the value passed to the URL param
    city_name = request.args.get('city')

    # Find the city code
    city_code = find_by_city_name(city_name)
    if not city_name:
        return jsonify({'success': False, 'error': 'City name required'}), 400
    
    try:
        result = api_client.get_current_weather(city_code)
        city_dict, weather_dict = result
        # city = City.from_dict(city_dict)
        # weather = Weather.from_dict(weather_dict)
        return jsonify({
            'success': True,
            'city': {
                'name': city_dict['city_name'],
                'country': city_dict['city_country'],
                'latitude': city_dict['city_lat'],
                'longitude': city_dict['city_lon']
            }, 'weather': {
                'temperature': weather_dict['temperature'],
                'feels_like': weather_dict['feel'],
                'min': weather_dict['temp_min'],
                'max': weather_dict['temp_max'],
                'description': weather_dict['description'],
                'humidity': weather_dict['humidity'],
                'wind_speed': weather_dict['wind_speed']
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400



if __name__ in "__main__":
    app.run(debug=True)