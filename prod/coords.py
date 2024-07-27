import pyproj
import requests


def itm_to_latlon(easting, northing):
    # Define the ITM projection (EPSG:2157)
    itm = pyproj.Proj(init="epsg:2157")

    # Define the WGS84 projection (EPSG:4326)
    wgs84 = pyproj.Proj(init="epsg:4326")

    # Convert ITM to Latitude/Longitude
    lon, lat = pyproj.transform(itm, wgs84, easting, northing)

    return lat, lon


def geocode_latlon(lat, lon, api_key):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={api_key}"

    response = requests.get(url)
    data = response.json()

    if data["results"]:
        address = data["results"][0]["formatted"]
        components = data["results"][0]["components"]
        eircode = components.get("postcode", "N/A")
        return address, eircode
    else:
        return None, None


# Example ITM coordinates
easting = 725830
northing = 734698

lat, lon = itm_to_latlon(easting, northing)

# Your OpenCage API key
api_key = "1ebff77e18ac4b9382c6498db39e5109"

address, eircode = geocode_latlon(lat, lon, api_key)
print(f"Address: {address}, Eircode: {eircode}")
