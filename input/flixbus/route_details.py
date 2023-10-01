import requests
import json
import re
import os

def load_from_json(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)
    
def fetch_global_api(url: str) -> dict:
    """Fetch data from a given URL."""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}. RESPONSE CODE: {response.status_code}")
    return response.json()

def is_valid_date(date_str):
    # Basic pattern check
    pattern = re.compile(r'^(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})$')
    match = pattern.match(date_str)
    
    if not match:
        return False
    
    day, month, year = map(int, [match['day'], match['month'], match['year']])
    
    # Check if year, month, and day are in valid ranges
    if not (1 <= month <= 12):
        return False

    if month in [1, 3, 5, 7, 8, 10, 12]:
        if not (1 <= day <= 31):
            return False
    elif month in [4, 6, 9, 11]:
        if not (1 <= day <= 30):
            return False
    else:  # February
        # Check for leap year
        is_leap = (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))
        if is_leap:
            if not (1 <= day <= 29):
                return False
        else:
            if not (1 <= day <= 28):
                return False

    return True

def convert_name_to_uuid(city_name, data_JSON):
    for item in data_JSON.values():
        if item["name"] == city_name:
            return item["id"]
    raise ValueError(f"'{city_name}' not found in the provided JSON.")

def route_details_URL_call(start_uuid, end_uuid, depature_date):
        # Check for valid UUID
        uuid_pattern = re.compile(r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$')
        if not uuid_pattern.match(start_uuid):
            raise ValueError(f"Invalid UUID format for start_uuid: {start_uuid}")
        if not uuid_pattern.match(end_uuid):
            raise ValueError(f"Invalid UUID format for end_uuid: {end_uuid}")
        if is_valid_date(depature_date) == False:
            raise ValueError(f"Invalid date format for departure_date: {depature_date}")
        
        url_template = (
            f"https://global.api.flixbus.com/search/service/v4/search?"
            f"from_city_id={start_uuid}&"
            f"to_city_id={end_uuid}&"
            f"departure_date={depature_date}&"
            f"products=%7B%22adult%22%3A1%7D&"
            f"currency=GBP&"
            f"locale=en_GB&"
            f"search_by=cities&"
            f"include_after_midnight_rides=1"
        )
        return url_template
    
def extract_route_details_from_json(data: dict) -> tuple:
    trip_details = []

    for trip in data["trips"]:
        for uid, result in trip["results"].items():
            # Now we are looking for results
            departure_station_id = result["departure"]["station_id"]
            arrival_station_id = result["arrival"]["station_id"]
            
            departure_station_name = data["stations"][departure_station_id]["name"]
            arrival_station_name = data["stations"][arrival_station_id]["name"]
            # Need logic to get departure city and arrival city name.
            departure_date = result["departure"]["date"]
            arrival_date = result["arrival"]["date"]
            price = result["price"]["total"]
            available_seats = result["available"]["seats"]
            provider = result["provider"]
            
            trip_details.append((departure_station_name, departure_date, arrival_station_name, arrival_date, price, available_seats, provider))

    return trip_details

def extract_journey_info(departure_name, arrival_name, date, bus_stops_JSON_path):
    if not is_valid_date(date):
        raise ValueError("Date given has incorrect format. Unable to make URL call.")
    # JSONS PATHS
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BUS_STOP_PATH = os.path.join(BASE_DIR, bus_stops_JSON_path)
    DANGER_TEMP_JSON_PATH = os.path.join(BASE_DIR, "route_details_temp.json") # Define here rather than parameter to prevent clearing wrong data
    
    # DATA FETCHING
    BUS_STOP_JSON_DATA = load_from_json(BUS_STOP_PATH)
    departure_id = convert_name_to_uuid(departure_name, BUS_STOP_JSON_DATA)
    arrival_id = convert_name_to_uuid(arrival_name, BUS_STOP_JSON_DATA)
    url_call = route_details_URL_call(departure_id, arrival_id, date)
    url_fetched_data = fetch_global_api(url_call)
    
    # LOGGING
    with open(DANGER_TEMP_JSON_PATH, 'w') as file: 
        json.dump(url_fetched_data, file) # May later want to append instead
    
    json_fetched_data = load_from_json(DANGER_TEMP_JSON_PATH)
    trip_details = extract_route_details_from_json(json_fetched_data)
    return trip_details
       