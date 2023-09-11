import os
import json
import requests
import re
import time
from unittest.mock import patch


def load_from_json(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)

def fetch_name_and_UUID_given_legacy_ID_from_JSON(legacy_id, JSON_bus_stop_path):
    data = load_from_json(JSON_bus_stop_path)
    entry = data.get(str(legacy_id), {})
    name = entry.get('name', None)
    uuid = entry.get('id', None)
    return name, uuid

def reachable_URL_call(uuid, limit=100):
    # Check for valid UUID
    uuid_pattern = re.compile(r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$')
    if not uuid_pattern.match(uuid):
        raise ValueError("Invalid UUID format")

    # Check for valid limit
    if not isinstance(limit, int) or limit <= 0 or limit > 200:
        raise ValueError("Limit must be a positive integer between 1 and 200")

    # Create the URL
    base_url = "https://global.api.flixbus.com/cms/cities/"
    params = f"{uuid.lower()}/reachable?language=en-gl&country=GB&limit={limit}"
    return base_url + params


def fetch_global_api(url: str) -> dict:
    """Fetch data from a given URL."""
    print(f"Request made at {url}", flush=True)
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}. RESPONSE CODE: {response.status_code}")
    return response.json()

def give_reachable_cities(json_data):    
    # Parse the JSON data if it's a string
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data

    # Extract city names and uuids from the "result" key where the country is 'GB', and create a dictionary out of them
    cities_dict = {city_info["name"]: city_info["uuid"] for city_info in data["result"] if city_info["country"] == "GB"}
    return cities_dict

def city_neighbours_entry(JSON_bus_stop_path, legacy_id_param, is_test_mode=False):
    name, uuid = fetch_name_and_UUID_given_legacy_ID_from_JSON(legacy_id_param, JSON_bus_stop_path)
    url = reachable_URL_call(uuid)
    try:
        fetched_data = fetch_global_api(url)
        reachable_cities_dict = give_reachable_cities(fetched_data)
        result = {
            str(legacy_id_param): {
                "name": name,
                "uuid": uuid,
                "neighbors": reachable_cities_dict
            }
        }
    except Exception as e:
        print(f"Error fetching data for city {name}. Error: {e}")
        result = None  # Setting to None if there's an error.

    if not is_test_mode:
        print("--- Delaying 2 Seconds Before Next Request ---")
        time.sleep(2)
    
    return result

def _difference_between_dictionaries(old_dict, new_dict):
    # Find keys that have been removed and added
    removed_keys = set(old_dict.keys()) - set(new_dict.keys())
    new_keys = set(new_dict.keys()) - set(old_dict.keys())
    
    # Create result dictionaries using dictionary comprehensions
    removed_entries = {key: old_dict[key] for key in removed_keys}
    new_entries = {key: new_dict[key] for key in new_keys}
    
    return {
        "removed_entries": removed_entries,
        "new_entries": new_entries
    }

class DataConflictException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def append_to_json(datatree, filename):
    # Read existing data from file
    with open(filename, 'r') as file:
        file_contents = file.read()
        existing_data = json.loads(file_contents) if file_contents.strip() else {}

    # Check for conflicts and merge data
    for city_id, city_info in datatree.items():
        if city_id in existing_data:
            for key, value in city_info.items():
                if key == "neighbors":
                    differences = _difference_between_dictionaries(existing_data[city_id].get(key, {}), value)
                    if differences["removed_entries"] or differences["new_entries"]:
                        raise Exception(f"Changes detected in neighbors for city ID {city_id}. Removed: {differences['removed_entries']}, Added: {differences['new_entries']}")
                if key in existing_data[city_id] and existing_data[city_id][key] != value:
                    # Conflict found
                    message = f"Conflict found for city ID {city_id} and key {key}. Existing: {existing_data[city_id][key]}, New: {value}."
                    print(message)  # Non-intrusive exception: Printing error message
                else:
                    existing_data[city_id][key] = value
        else:
            existing_data[city_id] = city_info

    # Write merged data back to the file
    with open(filename, 'w') as file:
        json.dump(existing_data, file, indent=4)


def create_flixbus_datatree(json_bus_stop_path, json_flixbus_tree_path, is_test_mode=False):
    with open(json_bus_stop_path, 'r') as file:
        bus_stop_contents = json.load(file)

    for legacy_id, city_info in bus_stop_contents.items():
        reachable_cities_tree = city_neighbours_entry(json_bus_stop_path, legacy_id, is_test_mode=True) # Set test mode to true so that we can see the delay here
        append_to_json(reachable_cities_tree, json_flixbus_tree_path)
        
        if not is_test_mode:
            print("--- Delaying 2 Seconds Before Next Request ---", flush=True)
            time.sleep(2)