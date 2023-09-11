import requests
import json
import re

def load_from_json(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)

def fetch_global_api(url: str) -> dict:
    """Fetch data from a given URL."""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}. RESPONSE CODE: {response.status_code}")
    return response.json()

def process_api_data(data: dict, target_language: str) -> list:
    relevant_data = []  # List to store relevant data
    
    # Define a recursive function to traverse nested structures
    def extract_relevant_data(item):
        if isinstance(item, dict):
            if "_language" in item and item["_language"] == target_language:
                relevant_data.append(item)
            for value in item.values():
                extract_relevant_data(value)
        elif isinstance(item, list):
            for element in item:
                extract_relevant_data(element)

    extract_relevant_data(data)  # Start the extraction process
    
    return relevant_data

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

def route_details_URL_call(start_uuid, end_uuid, depature_data):
        # Check for valid UUID
        uuid_pattern = re.compile(r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$')
        if not uuid_pattern.match(start_uuid):
            raise ValueError(f"Invalid UUID format for start_uuid: {start_uuid}")
        if not uuid_pattern.match(end_uuid):
            raise ValueError(f"Invalid UUID format for end_uuid: {end_uuid}")
        if is_valid_date(depature_data) == False:
            raise ValueError(f"Invalid date format for departure_date: {depature_data}")
        
        url_template = (
            f"https://global.api.flixbus.com/search/service/v4/search?"
            f"from_city_id={start_uuid}&"
            f"to_city_id={end_uuid}&"
            f"departure_date={depature_data}&"
            f"products=%7B%22adult%22%3A1%7D&"
            f"currency=GBP&"
            f"locale=en_GB&"
            f"search_by=cities&"
            f"include_after_midnight_rides=1"
        )
        return url_template