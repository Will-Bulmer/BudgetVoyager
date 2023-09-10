import os
import json
import requests
import time

def save_to_json(data: dict, file_path: str) -> None:
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_from_json(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)

def create_fetch_name_and_UUID_URL(legacy_id : int) -> str:
    # Check for valid UUID
    if not isinstance(legacy_id, int) or legacy_id <= 0:
        raise ValueError("legacy_id must be a positive integer.")
    base_url = f"https://global.api.flixbus.com/search/service/cities/details?locale=en_GB&from_city_id={legacy_id}"
    return base_url

def fetch_global_api(url: str) -> dict:
    """Fetch data from a given URL."""
    print(f"Request made at {url}")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}. RESPONSE CODE: {response.status_code}")
    return response.json()

def extract_name_and_UUID(data: dict) -> tuple:
    # Check Input Data Format
    if not data or not isinstance(data, list) or len(data) == 0:
        raise ValueError("Data should be a non-empty list of dictionaries.")
    keys = ['name', 'id', 'legacy_id']
    if not all(key in data[0] for key in keys):
        raise ValueError("Data is missing essential keys.")
    return data[0]['legacy_id'], data[0]['name'], data[0]['id']

def append_name_and_UUID(legacy_id, city_name, city_id, file_path):
    data = load_from_json(file_path)
    if str(legacy_id) in data:
        entry = data[str(legacy_id)]
        # Data attached to each legacy_id must be a dictionary
        if not isinstance(entry, dict):
            raise TypeError("Invalid data structure for entry.")
        entry.update({'name': city_name, 'id': city_id})
    else:
        raise KeyError(f"No entry found for legacy_id: {legacy_id}")
    save_to_json(data, file_path)
    return data

def create_fetch_location_URL(name : str) -> str:
    # Check for valid UUID
    if not isinstance(name, str):
        raise ValueError("name must be a String.")
    base_url = f"https://global.api.flixbus.com/search/autocomplete/cities?q={name}&lang=en&country=gb&flixbus_cities_only=false&stations=false"
    return base_url

def extract_lat_and_lon(data: list) -> tuple:
    # Check Input Data Format
    if not data or not isinstance(data, list) or len(data) == 0:
        raise ValueError("Data should be a non-empty list of dictionaries.")
    if not isinstance(data[0], dict):
        raise ValueError("The first item in the list should be a dictionary.")
    location = data[0].get('location', {})
    if 'lat' not in location or 'lon' not in location:
        raise ValueError("Data is missing lat or lon.")
    return location['lat'], location['lon']

def append_lat_and_lon(legacy_id, lat, lon, file_path):
    data = load_from_json(file_path)
    if str(legacy_id) not in data:
        raise KeyError(f"No entry found for legacy_id: {legacy_id}")
    data[str(legacy_id)]['location'] = {'lat': lat, 'lon': lon}
    save_to_json(data, file_path)
    return data

def update_bus_stops(JSON_file_path, is_test_mode=False):
    data = load_from_json(JSON_file_path)
    
    # Iterate through each legacy_id and update the name and UUID
    for legacy_id, entry in data.items():
        url = create_fetch_name_and_UUID_URL(int(legacy_id))
        api_data = fetch_global_api(url)
        legacy_id, city_name, city_id = extract_name_and_UUID(api_data)
        append_name_and_UUID(int(legacy_id), city_name, city_id, JSON_file_path)
        # Only introduce delay if not in test mode
        if not is_test_mode:
            print("--- Delaying 2 Seconds Before Next Request ---")
            time.sleep(2)

    # Iterate through each name and update the latitude and longitude
    for legacy_id, entry in data.items():
        city_name = entry["name"]

        # Fetch the latitude and longitude for the name
        url = create_fetch_location_URL(city_name)
        api_data = fetch_global_api(url)
        lat, lon = extract_lat_and_lon(api_data)
        append_lat_and_lon(int(legacy_id), lat, lon, JSON_file_path)
        # Only introduce delay if not in test mode
        if not is_test_mode:
            print("--- Delaying 2 Seconds Before Next Request ---")
            time.sleep(2)

