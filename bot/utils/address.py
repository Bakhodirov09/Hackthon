from geopy.geocoders import Nominatim


async def get_address(latitude: float, longitude: float):
    geolocator = Nominatim(user_agent="ecogram")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    json = location.raw

    return (f"{((json['address']['road'] + ', ') if 'road' in json['address'] else json['name'])}"
            f"{(json['address']['county'] + ', ') if 'county' in json['address'] else ''}"
            f"{json['address']['city']}, {json['address']['country']}")
