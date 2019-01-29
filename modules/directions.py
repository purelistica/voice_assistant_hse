import requests
import json
from urllib.parse import urlencode
from modules import auth_keys


def get_directions(origin, destination, mode='driving'):
    """Accepts coordinates only for now"""
    params = {'origin': to_point(origin), 'destination': to_point(destination),
              'mode': mode, 'departure_time': 'now', 'key': auth_keys.key}
    link = 'https://maps.googleapis.com/maps/api/directions/json?'
    url = link + urlencode(params)
    r = requests.get(url)
    result = json.loads(r.text)
    if result['status'] == "OK":
        return result['routes']
    else:
        return None


def to_point(latlng):
    point = str(latlng['lat']) + ',' + str(latlng['lng'])
    return point


def route_duration(routes):
    leg = routes[0]['legs'][0]
    if 'duration_in_traffic' in leg:
        dur = leg['duration_in_traffic']['value']
    else:
        dur = leg['duration']['value']
    minutes = round(dur/60)
    return minutes
