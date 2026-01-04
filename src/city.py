class City:
    def __init__(self, name, country, coordinate):
        self.name = name
        self.country = country
        self.coordinate = coordinate

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['city_name'],
            country=data['city_country'],
            coordinate={
                'latitude': data['city_lat'],
                'longitude': data['city_lon']
            }
        )