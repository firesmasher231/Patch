import requests
from bs4 import BeautifulSoup
from pyproj import Proj, transform

# Define the ITM and WGS84 projections
itm_proj = Proj(init='epsg:2157')  # ITM projection
wgs84_proj = Proj(init='epsg:4326')  # WGS84 projection

def itm_to_latlon(easting, northing):
    lon, lat = transform(itm_proj, wgs84_proj, easting, northing)
    return lat, lon

def fetch_eircode_from_gridfinder(lat, lon):
    url = f'https://irish.gridreferencefinder.com/?gr={lat},{lon}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the element that contains the Eircode
    eircode_elem = soup.find(text="Eircode:").findNext('td').text
    
    if eircode_elem:
        return eircode_elem.strip()
    else:
        raise Exception('Eircode not found on the page')

def itm_to_eircode(easting, northing):
    lat, lon = itm_to_latlon(easting, northing)
    eircode = fetch_eircode_from_gridfinder(lat, lon)
    return eircode

# Example usage:
easting = 709825
northing = 736743

try:
    eircode = itm_to_eircode(easting, northing)
    print(f'The Eircode is: {eircode}')
except Exception as e:
    print(e)
