import requests
import pytest
from unittest.mock import patch, Mock
import unittest
import json
import os
import tempfile
import create_flixbus_tree


class TestFetchGlobalApi:
    @patch('requests.get')
    def test_successful_response(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'test_key': 'test_value'}
        mock_get.return_value = mock_response

        url = 'https://example.com/api'
        response_data = create_flixbus_tree.fetch_global_api(url)

        assert response_data == {'test_key': 'test_value'}

    @patch('requests.get')
    def test_failed_response(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        url = 'https://example.com/api'
        with pytest.raises(Exception):
            create_flixbus_tree.fetch_global_api(url)

# Behavioural Test            
class TestNeighbouringCities:
    def test_give_reachable_cities_othery(self):
        # Sample input data
        json_data = {
            "result": [
                {
                    "country": "GB",
                    "id": 3848,
                    "language": "en-gl",
                    "location": {
                        "lat": 51.50735,
                        "lon": -0.1277583
                    },
                    "name": "London",
                    "search_volume": 1933100,
                    "slug": "london",
                    "transportation_category": ["bus"],
                    "uuid": "40dfdfd8-8646-11e6-9066-549f350fcb0c"
                }
            ],
            "count": 1
        }
        # Expected output
        expected = {"London" : "40dfdfd8-8646-11e6-9066-549f350fcb0c"}
        
        # Check if the function's output matches the expected output
        assert expected == create_flixbus_tree.give_reachable_cities(json_data)
    

    def test_give_reachable_cities_hayle(self):
        # Get the directory of the current script
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the JSON file
        JSON_PATH = os.path.join(BASE_DIR, "hayle_nearby.json")
        # Read the data from the JSON file
        with open(JSON_PATH, 'r') as file:
            json_data = json.load(file)
        
        # Expected output based on the provided data
        expected = {
            "London": "40dfdfd8-8646-11e6-9066-549f350fcb0c",
            #"Amsterdam": "40dde3b8-8646-11e6-9066-549f350fcb0c",
            "Birmingham": "5415b966-f8b8-4b27-8620-1641c1a43e45",
            "Bristol": "8aa5378a-5f22-429c-88f7-2468ffab2757",
            "Newcastle upon Tyne": "88a001c8-eaf6-4126-9ab4-9c0790561e20",
            "Sheffield": "7e720125-5f82-450f-b4cc-ac68935a5b62",
            "Nottingham": "f1d39e6c-8e93-4987-b662-0a962140eae8",
            "Heathrow Airport": "3ed3bb14-b327-4fd8-8a12-465b08ae886d",
            "Liverpool": "b7e2b915-e36a-4df8-821d-2e5a7ef48889",
            "London Gatwick Airport": "1a716b56-a361-4946-89a0-34a6424532e9",
            "Plymouth": "8e6f0212-5248-441d-8a3f-9bd653fa54c5",
            "Reading": "9c211de9-c1f3-4ac1-92fa-8913f7b963f4",
            "Exeter": "37270b23-e4a9-45e3-92a6-06bd94ed417b",
            "Taunton": "012b776f-8b2a-4ff8-bf22-ff2a90f8a049",
            "Newquay": "6c851f9e-cb08-4f7e-a0ac-9e83a9990045"
        }
        
        # Check if the function's output matches the expected output
        assert expected == create_flixbus_tree.give_reachable_cities(json_data)   
        
class TestURLCall:
    def test_reachable_URL_call(self):
        # Example UUID
        input_uuid = "6f51bf86-01a6-423d-ac31-e35277829e91"
        # Number of gets displayed
        limit = 100
        # Base and dynamic parts of the URL
        base_url = "https://global.api.flixbus.com/cms/cities/"
        endpoint = "/reachable"
        params = "?language=en-gl&country=GB&limit={}"

        # Construct the expected URL using string formatting
        expected_url = "{}{}{}{}".format(base_url, input_uuid, endpoint, params.format(limit))
        
        # Get the actual URL from the function
        actual_url = create_flixbus_tree.reachable_URL_call(input_uuid)
        
        # Assert that the expected URL matches the actual URL
        assert expected_url == actual_url, f"Expected URL: {expected_url}, but got: {actual_url}"
        
    def test_standard_UUID(self):
        input = "6f51bf86-01a6-423d-ac31-e35277829e91"
        limit = 100
        output = "https://global.api.flixbus.com/cms/cities/6f51bf86-01a6-423d-ac31-e35277829e91/reachable?language=en-gl&country=GB&limit=100"
        assert output == create_flixbus_tree.reachable_URL_call(input, limit)

    def test_invalid_UUID_format(self):
        with pytest.raises(ValueError):
            create_flixbus_tree.reachable_URL_call("abcd-1234-efgh")

    def test_empty_UUID(self):
        with pytest.raises(ValueError):
            create_flixbus_tree.reachable_URL_call("")

    def test_special_char_UUID(self):
        with pytest.raises(ValueError):
            create_flixbus_tree.reachable_URL_call("1234-5678-9abc-def$")

    def test_case_sensitivity(self):
        input_lower = "a1b2c3d4-e5f6-7a8b-9c0d-ef1234567890"
        input_upper = "A1B2C3D4-E5F6-7A8B-9C0D-EF1234567890"
        limit = 100
        output = "https://global.api.flixbus.com/cms/cities/a1b2c3d4-e5f6-7a8b-9c0d-ef1234567890/reachable?language=en-gl&country=GB&limit=100"
        assert output == create_flixbus_tree.reachable_URL_call(input_lower, limit)
        assert output == create_flixbus_tree.reachable_URL_call(input_upper, limit)

    def test_non_integer_limit(self):
        input = "6f51bf86-01a6-423d-ac31-e35277829e91"
        with pytest.raises(ValueError):
            create_flixbus_tree.reachable_URL_call(input, "forty")

    def test_float_limit(self):
        input = "6f51bf86-01a6-423d-ac31-e35277829e91"
        with pytest.raises(ValueError):
            create_flixbus_tree.reachable_URL_call(input, 40.5)

    def test_negative_limit(self):
        input = "6f51bf86-01a6-423d-ac31-e35277829e91"
        with pytest.raises(ValueError):
            create_flixbus_tree.reachable_URL_call(input, -10)

    def test_no_limit(self):
        input = "6f51bf86-01a6-423d-ac31-e35277829e91"
        output = "https://global.api.flixbus.com/cms/cities/6f51bf86-01a6-423d-ac31-e35277829e91/reachable?language=en-gl&country=GB&limit=100"  # Assuming 40 is the default limit
        assert output == create_flixbus_tree.reachable_URL_call(input)

    def test_large_limit(self):
        input_uuid = "6f51bf86-01a6-423d-ac31-e35277829e91"
        limit = 1000000000
        with pytest.raises(ValueError):
            create_flixbus_tree.reachable_URL_call(input_uuid, limit)


def mock_reachable_URL_call(uuid):
    return f"https://global.api.flixbus.com/cms/cities/{uuid}/reachable?language=en-gl&country=GB&limit=40"
def mock_fetch_global_api(url):
    return {"cities": [{"name": "CityB", "uuid": "UUID_B"}, {"name": "CityC", "uuid": "UUID_C"}]}
def mock_give_reachable_cities(fetched_data):
    return {city["name"]: city["uuid"] for city in fetched_data["cities"]}


class TestCreateFlixbusDatatree(unittest.TestCase):
    
    @patch('create_flixbus_tree.reachable_URL_call', side_effect=mock_reachable_URL_call)
    @patch('create_flixbus_tree.fetch_global_api', side_effect=mock_fetch_global_api)
    @patch('create_flixbus_tree.give_reachable_cities', side_effect=mock_give_reachable_cities)
    def test_create_flixbus_datatree(self, mock_reachable_URL_call, mock_fetch_global_api, mock_give_reachable_cities):
        
        sample_data = {
            "CityA": {"uuid": "UUID_A"},
            "CityX": {}  # This city has no UUID, so it should be ignored
        }
        
        expected_datatree = {
            "CityA": {
                "uuid": "UUID_A",
                "neighbors": {
                    "CityB": "UUID_B",
                    "CityC": "UUID_C"
                }
            }
        }
        
        result_datatree = create_flixbus_tree.create_flixbus_datatree(sample_data, max_entries = 10, is_test_mode=True,)
        self.assertEqual(result_datatree, expected_datatree)


class TestAppendTreeToJson:

    @pytest.fixture
    def temp_json_file(self):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file_name = temp_file.name
        temp_file.close()
        
        # Provide the temp file name to the test function
        yield temp_file_name
        
        # After the test function completes, delete the temp file
        os.remove(temp_file_name)

    # Utility method to write initial data
    def _write_initial_data(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f)

    # Utility method to read data from file
    def _read_data(self, filename):
        with open(filename, 'r') as f:
            return json.load(f)

    def test_append_to_json(self, temp_json_file):
        self._write_initial_data({
            "CityA": {"name": "CityA", "uuid": "UUID_A", "neighbors": {}}
        }, temp_json_file)

        # Data to append
        datatree = {"CityB": {"name": "CityB", "neighbors": {"CityC": "UUID_C"}}}
        
        create_flixbus_tree.append_to_json(datatree, temp_json_file)
        updated_data = self._read_data(temp_json_file)
        
        # Check CityA data remains unchanged
        assert updated_data["CityA"] == {"name": "CityA", "uuid": "UUID_A", "neighbors": {}}
        # Check CityB was added
        assert updated_data["CityB"] == {"name": "CityB", "neighbors": {"CityC": "UUID_C"}}
    
    def test_append_conflicting_data(self, temp_json_file):
        self._write_initial_data({
            "CityA": {"name": "CityA", "uuid": "UUID_A", "neighbors": {"CityD": "UUID_D"}}
        }, temp_json_file)

        # Data with conflicting information
        datatree = {"CityA": {"name": "CityA_NEW", "uuid": "UUID_A_NEW", "neighbors": {"CityC": "UUID_C"}}}
        
        create_flixbus_tree.append_to_json(datatree, temp_json_file)
        updated_data = self._read_data(temp_json_file)

        # Check that conflicting data was overwritten
        assert updated_data["CityA"] == {"name": "CityA_NEW", "uuid": "UUID_A_NEW", "neighbors": {"CityD": "UUID_D", "CityC": "UUID_C"}}
    
    def test_appending_to_empty_file(self, temp_json_file):
        self._write_initial_data({}, temp_json_file)
        
        datatree = {"CityE": {"name": "CityE", "uuid": "UUID_E", "neighbors": {}}}
        create_flixbus_tree.append_to_json(datatree, temp_json_file)
        updated_data = self._read_data(temp_json_file)

        assert updated_data["CityE"] == {"name": "CityE", "uuid": "UUID_E", "neighbors": {}}

    def test_appending_empty_data(self, temp_json_file):
        self._write_initial_data({
            "CityK": {"name": "CityK", "uuid": "UUID_K", "neighbors": {}}
        }, temp_json_file)

        create_flixbus_tree.append_to_json({}, temp_json_file)
        updated_data = self._read_data(temp_json_file)

        assert updated_data["CityK"] == {"name": "CityK", "uuid": "UUID_K", "neighbors": {}}
    
    def test_data_with_missing_name_or_uuid(self, temp_json_file):
        create_flixbus_tree.append_to_json({"CityL": {"neighbors": {"CityM": "UUID_M"}}}, temp_json_file)
        updated_data = self._read_data(temp_json_file)

        assert updated_data["CityL"]["name"] == "CityL"
        assert "uuid" not in updated_data["CityL"]






