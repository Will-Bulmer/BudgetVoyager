#!/usr/bin/python3

import os
import sys
import json
import _can_webscrape
import flixbus_scrape
import create_flixbus_tree

def make_flixbus_routes():
    # Get the directory containing your_current_file.py
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Go up two directories (first to src, then to project_root) and then navigate to the desired file
    JSON_ID_PATH = os.path.join(BASE_DIR, '..', 'input', 'flixbus_tree', 'flixbus_ID.json')
    JSON_tree_PATH = os.path.join(BASE_DIR, '..', 'input', 'flixbus_tree', 'flixbus_tree.json')

    # Read the JSON data from the file
    with open(JSON_ID_PATH, 'r') as json_file:
        json_data = json.load(json_file)

    datatree = create_flixbus_tree.create_flixbus_datatree(json_data, max_entries=100, is_test_mode=False,)
    create_flixbus_tree.append_to_json(datatree, JSON_tree_PATH)
    


def main():
    #print(sys.path)
    make_flixbus_routes()

if __name__ == "__main__":
    main()




