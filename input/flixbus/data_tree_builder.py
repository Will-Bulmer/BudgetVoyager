import os
import json
import requests
import re
import time


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
    print(f"Request made at {url}")
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

def create_flixbus_datatree(json_data, max_entries, is_test_mode=False):
    datatree = {}
    entry_count = 0  # Counter to keep track of processed entries
    
    # Loop through each city in the provided JSON data
    for city_name, city_info in json_data.items():
        # Check if the city has a UUID
        if "uuid" in city_info:
            # Create the API URL for the given UUID
            url = reachable_URL_call(city_info["uuid"])
            
            try:
                # Fetch the JSON data from the API
                fetched_data = fetch_global_api(url)
                
                # Extract the names and UUIDs of the reachable cities from the fetched data
                reachable_cities = give_reachable_cities(fetched_data)
                #print(f'Found Nodes : {reachable_cities}')
                
                # Add the reachable cities to the data tree
                datatree[city_name] = {
                    "uuid": city_info["uuid"],
                    "neighbors": reachable_cities
                }
                #print(f'Datatree Created : {datatree}')
                
                entry_count += 1  # Increment the counter
                
                if entry_count >= max_entries:
                    break  # Exit the loop if the maximum entries limit is reached
            
            except Exception as e:
                print(f"Error fetching data for city {city_name}. Error: {e}")
            
            # Only introduce delay if not in test mode
            if not is_test_mode:
                print("--- Delaying 2 Seconds Before Next Request ---")
                time.sleep(2)
    
    return datatree

def append_to_json(datatree, filename):
    # Check if file is empty
    with open(filename, 'r') as file:
        file_contents = file.read()
        if not file_contents.strip():
            existing_data = {}
        else:
            existing_data = json.loads(file_contents)

    # Update the existing data with the new data (datatree)
    for city_name, city_info in datatree.items():
        city_name_cleaned = city_name.strip().lower()

        if city_name_cleaned not in existing_data:
            print(f"Appending data for city: {city_name}")
            existing_data[city_name_cleaned] = {
                "name": city_name,
                "neighbors": city_info.get("neighbors", {})
            }
            if "uuid" in city_info:
                existing_data[city_name_cleaned]["uuid"] = city_info["uuid"]
        else:
            print(f"Updating data for city: {city_name}")
            if "name" in city_info:
                existing_data[city_name_cleaned]['name'] = city_info["name"]
            if "uuid" in city_info:
                existing_data[city_name_cleaned]['uuid'] = city_info["uuid"]
            if "neighbors" in city_info:
                existing_data[city_name_cleaned]['neighbors'].update(city_info["neighbors"])

    # Write the updated data back to the file
    with open(filename, 'w') as file: 
        json.dump(existing_data, file, indent=4)
