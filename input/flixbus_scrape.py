# File for webscraping flixbus
# Minimal requests and timed
import requests

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
