from icecream import ic


def get_distance_miles(loc1, loc2):
    if loc1: loc1 = float(loc1)
    if loc2: loc2 = float(loc2)

    from geopy.distance import geodesic
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent='measurements')
    destination1 = None
    destination2 = None

    if loc1 and loc2:
        destination1 = geolocator.geocode(loc1)
        destination2 = geolocator.geocode(loc2)
    if destination1 and destination1:
        distance = geodesic((destination1.latitude, destination1.longitude), (destination2.latitude, destination2.latitude))
        distance = round(distance.miles, 2)
        return distance
