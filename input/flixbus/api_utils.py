import os
import json
import requests
import time


class WriteToReadOnlyFileError(Exception):
    """Exception raised when attempting to write to a read-only file."""
    pass

def save_to_json(data: dict, file_path: str) -> None:
    # Check if file is writable
    if os.path.exists(file_path) and not os.access(file_path, os.W_OK):
        raise WriteToReadOnlyFileError(f"Cannot write to a read-only file: {file_path}")
    
    try:
        with open(file_path, 'w') as file:
            formatted_data = ',\n'.join(f'"{key}": {json.dumps(value)}' for key, value in data.items())
            file.write('{' + '\n')
            file.write(formatted_data)
            file.write('\n' + '}')
    except Exception as e:
        raise e

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
    name = name.replace(" ", "-") #Remove Spaces
    base_url = f"https://global.api.flixbus.com/search/autocomplete/cities?q={name}&lang=en&country=gb&flixbus_cities_only=false&stations=false"
    return base_url

def extract_lat_and_lon(data: list, legacy_id: int) -> tuple:
    # Check Input Data Format
    if not data or not isinstance(data, list) or len(data) == 0:
        raise ValueError("Data should be a non-empty list of dictionaries.")
    
    # Find the dictionary with the matching legacy_id
    matching_data = next((item for item in data if isinstance(item, dict) and item.get("legacy_id") == legacy_id), None)
    if not matching_data:
        raise ValueError(f"No matching data found for legacy_id {legacy_id}.")
    
    location = matching_data.get('location', {})
    if 'lat' not in location or 'lon' not in location:
        raise ValueError("Data is missing lat or lon.")
    return location['lat'], location['lon']

def append_lat_and_lon(legacy_id, lat, lon, file_path):
    data = load_from_json(file_path)
    if str(legacy_id) not in data and int(legacy_id) not in data:
        raise KeyError(f"No entry found for legacy_id: {legacy_id}")
    data[str(legacy_id)]['location'] = {'lat': lat, 'lon': lon}
    save_to_json(data, file_path)
    return data

def _update_data(data, JSON_file_path, url_callback, extract_callback, append_callback, is_test_mode):
    for legacy_id, entry in data.items():
        try:
            url = url_callback(legacy_id, entry)
            api_data = fetch_global_api(url)
            extracted_data = extract_callback(api_data, legacy_id)
            append_callback(*extracted_data, JSON_file_path)
        except Exception as e:
            print(f"Failed to process legacy_id : {legacy_id}. Error: {e}")
            continue 

        if not is_test_mode:
            print("--- Delaying 2 Seconds Before Next Request ---", flush=True)
            time.sleep(2)

# Callbacks
def url_for_name_and_UUID(legacy_id, entry):
    return create_fetch_name_and_UUID_URL(int(legacy_id))
def url_for_location(legacy_id, entry):
    city_name = entry["name"]
    print(entry)
    return create_fetch_location_URL(city_name)

def extract_for_name_and_UUID(api_data, legacy_id):
    legacy_id, city_name, city_id = extract_name_and_UUID(api_data)
    return str(legacy_id), city_name, city_id
def extract_for_location(api_data, legacy_id):
    lat, lon = extract_lat_and_lon(api_data, int(legacy_id))
    return int(legacy_id), lat, lon
    
def update_bus_stops(JSON_file_path, is_test_mode=False):
    data = load_from_json(JSON_file_path)
    _update_data(data, JSON_file_path, url_for_name_and_UUID, extract_for_name_and_UUID, append_name_and_UUID, is_test_mode)
    # Reload data after the first update
    data = load_from_json(JSON_file_path)
    _update_data(data, JSON_file_path, url_for_location, extract_for_location, append_lat_and_lon, is_test_mode)

    
 




