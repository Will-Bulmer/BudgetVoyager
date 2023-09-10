#!/usr/bin/python3

import os
import sys
import json
import _can_webscrape
from flixbus import api_utils
from flixbus import data_tree_builder
from flixbus import route_details

def make_flixbus_city_info():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    JSON_ID_PATH = os.path.join(BASE_DIR, '..', 'input', 'flixbus', 'bus_stops.json')
    
    # Read the JSON data from the file
    with open(JSON_ID_PATH, 'r') as json_file:
        json_data = json.load(json_file)

    # Update the file directly
    api_utils.update_bus_stops(JSON_ID_PATH, is_test_mode=False)
    
def make_flixbus_routes():
    # Get the directory containing your_current_file.py
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Go up two directories (first to src, then to project_root) and then navigate to the desired file
    JSON_ID_PATH = os.path.join(BASE_DIR, '..', 'input', 'flixbus_tree', 'flixbus_ID.json')
    JSON_tree_PATH = os.path.join(BASE_DIR, '..', 'input', 'flixbus_tree', 'flixbus_tree.json')

    # Read the JSON data from the file
    with open(JSON_ID_PATH, 'r') as json_file:
        json_data = json.load(json_file)

    datatree = data_tree_builder.create_flixbus_datatree(json_data, max_entries=100, is_test_mode=False,)
    data_tree_builder.append_to_json(datatree, JSON_tree_PATH)
    


def main():
    #print(sys.path)
    #make_flixbus_routes()
    make_flixbus_city_info()

if __name__ == "__main__":
    main()




