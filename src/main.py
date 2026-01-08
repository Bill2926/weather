import os
from api_client import API_Client
from config import Config
from weather import Weather
from city import City, find_by_city_name, find_by_city_code
from day_forecast_weather import DayForecastWeather

# Initialization
config = Config.load()
api_client = API_Client(config.base_url, config.daily_url, config.geocoding_url, config.api_key)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Display application header"""
    print("\n" + "=" * 60)
    print("🌤️  WEATHER API v1.0".center(60))
    print("=" * 60 + "\n")

def get_city_input():
    """Get city name from user"""
    print("Enter city name (or 'exit' to quit):")
    city_name = input("🔍 > ").strip()
    return city_name

def get_weather_type_choice():
    """Ask user what type of weather information they want"""
    print("What would you like to see?")
    print("1. Current weather")
    print("2. Weather forecast")
    choice = input("Choose (1 or 2): ").strip()
    return choice

def get_forecast_days():
    """Ask user how many days of forecast they want (1-16)"""
    while True:
        try:
            print("\nHow many days of forecast? (1-16)")
            days = int(input("Days > ").strip())
            if 1 <= days <= 16:
                return days
            else:
                print("⚠️ Please enter a number between 1 and 16.")
        except ValueError:
            print("⚠️ Please enter a valid number.")

def show_current_weather(city_code):
    """Fetch and display current weather information for a city"""
    try:
        result = api_client.get_current_weather(city_code)
        city_dict, weather_dict = result
        
        city = City.from_dict(city_dict)
        weather = Weather.from_dict(weather_dict)
    
        print("\n" + "=" * 60)
        print("📍 CURRENT WEATHER".center(60))
        print("=" * 60 + "\n")
        weather.display_weather()
        city.display_city()
        
        return True
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        return False

def show_forecast_weather(city_name, days):
    """Fetch and display forecast weather for a city"""
    try:
        coordinates = api_client.get_geocoding(city_name)
        if not coordinates:
            print(f"\n❌ Could not find city {city_name}.")
            return False

        forecast_data = api_client.get_day_forecast(coordinates, days)
        if not forecast_data:
            print(f"\n❌ Could not retrieve forecast data.")
            return False
        
        print("\n" + "=" * 60)
        print(f"📊 {days}-DAY WEATHER FORECAST FOR {city_name.upper()}".center(60))
        print("=" * 60 + "\n")
            
        for forecast_dict in forecast_data:
            forecast = DayForecastWeather.from_dict(forecast_dict)
            forecast.display_day_forecast_weather()
        return True
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        return False

def main():
    """Main application loop"""
    clear_screen()
    print_header()
    print("Welcome! Get weather information for any city.\n")
    
    while True:
        choice = get_weather_type_choice()
        if choice == '1':
            # Show current weather
            city_name = get_city_input()
            if city_name == "exit":
                clear_screen()
                print_header()
                continue
            city_code = find_by_city_name(city_name)
            success = show_current_weather(city_code)
        elif choice == '2':
            # Show forecast
            city_name = get_city_input()
            if city_name == "exit":
                clear_screen()
                print_header()
                continue
            days = get_forecast_days()
            success = show_forecast_weather(city_name, days)
        elif choice.lower() in ['exit', 'quit', 'q', '0']:
            print("\n👋 Thank you for using Weather API. Goodbye!\n")
            break
        elif not choice:
            clear_screen()
            print_header()
            print("⚠️ Please enter a valid input.\n")
            continue
        else:
            clear_screen()
            print_header()
            print("⚠️ Invalid choice. Please enter 1 or 2.\n")
            continue

        if not success:
            input("\nPress enter to continue...")
            clear_screen()
            print_header()
            continue
        
        # Ask if user wants to continue
        print("\n" + "=" * 60)
        input("\nPress Enter to search another city...")
        clear_screen()
        print_header()

if __name__ == "__main__":
    main()