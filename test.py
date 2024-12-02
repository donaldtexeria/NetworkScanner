import http.client
import subprocess
import maxminddb
from geopy.geocoders import Nominatim

import urllib.parse

def reverse_geocode(lat, lon):
    geolocator = Nominatim(user_agent="donda")
    location = geolocator.reverse((lat, lon), language='en')
    if location:
        address = location.raw.get('address', {})
        city = address.get('city', None)
        state = address.get('state', None)
        country = address.get('country', None)
        ans = ""
        if city:
            ans += city + ", "
        if state:
            ans += state + ", "
        if country:
            ans += country
            
        return ans
    else:
        return

def get_geo_locations(ips):
    locations = set()
    for ip in ips:
        with maxminddb.open_database("GeoLite2-City.mmdb") as reader:
            loc_info = reader.get(ip)
            lat = float(loc_info["location"]["latitude"])
            lon = float(loc_info["location"]["longitude"])
            location = reverse_geocode(lat, lon)
            locations.add(location)
    return list(locations)
    
            


if __name__ == "__main__":
    ips = [
            "129.105.136.48"
        ]
    locations = get_geo_locations(ips)
    print(locations)