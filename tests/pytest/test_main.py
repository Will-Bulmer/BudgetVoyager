import pytest
import os
import json
import main

class TestFlixbusRouteCreation:
    def test_filepath(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        expected_path = os.path.join(BASE_DIR, '..', '..', 'input', 'flixbus', 'bus_stops.json')
        assert os.path.exists(expected_path)

