import json
from pathlib import Path

city_list_path = Path(__file__).parent.parent /'external_data'/'city.list.json'

def find_by_city_name(city_name):
    with open(city_list_path, 'r', encoding='utf-8') as f:
        city_code_data = json.load(f)
        result_list = []
        for c in city_code_data:
            if city_name.strip().lower() in c['name'].lower():
                result_list.append(
                    {
                        'id': c['id'],
                        'city_name': c['name'],
                        'country': c['country']
                    }
                )
        
        if len(result_list) == 1:
            return result_list[0]['id']
        elif len(result_list) == 0:
            return False
        else:
            i = 1
            for r in result_list:
                
                print(f"{i}. {r['city_name']} / {r['country']}")
                i += 1
            print('Please choose your prefered city:')
            choice = int(input("> "))
            if choice:
                return result_list[choice-1]['id']

def find_by_city_code(city_code):
    with open(city_list_path, 'r', encoding='utf-8') as f:
        city_code_data = json.load(f)
        for c in city_code_data:
            if c["id"] == city_code:
                return c["name"]

class City:
    def __init__(self, name, country, coordinate):
        self.name = name
        self.country = country
        self.coordinate = coordinate

    def display_city(self):
        print("=" * 50)
        print(f"📍 CITY INFORMATION")
        print("=" * 50)
        print(f"  City:      {self.name}")
        print(f"  Country:   {self.country}")
        print(f"  Latitude:  {self.coordinate['latitude']}°")
        print(f"  Longitude: {self.coordinate['longitude']}°")
        print("=" * 50 + "\n")

    @classmethod
    def from_dict(cls, data):
        country_iso_path = Path(__file__).parent.parent /'external_data'/'iso_country_codes.json'
        country_full_name = data['city_country']
        with open(country_iso_path, 'r', encoding='utf-8') as f:
            country_code = json.load(f)
            for c in country_code:
                if country_full_name == c['code']:
                    country_full_name = f"{c['name']} ({c['code']})"

        return cls(
            name=data['city_name'],
            country=country_full_name,
            coordinate={
                'latitude': data['city_lat'],
                'longitude': data['city_lon']
            }
        )