import requests
import pytest
from unittest.mock import patch, Mock
import unittest
import json
import os
import tempfile
import data_tree_builder


# Test for fetch_UUID_given_legacy_ID()
def mock_bus_stop_content(url):
    return {
    "60151": {"name": "Aberdeen", "id": "4588b4ab-79ea-4c6d-88ae-30b58611f263", "location": {"lat": 57.149717, "lon": -2.094278}},
    "51081": {"name": "Amesbury", "id": "ce39aa68-df35-4462-a239-1edd92241574", "location": {"lat": 51.1679201, "lon": -1.7629783}},
    "14668": {"name": "Birmingham", "id": "5415b966-f8b8-4b27-8620-1641c1a43e45", "location": {"lat": 52.4829, "lon": -1.8936}},
    "46591": {"name": "Bradford", "id": "97b09a17-671e-4ce2-a62f-dd4a7022f98f", "location": {"lat": 53.795984, "lon": -1.759398}},
    "47351": {"name": "Bridgend", "id": "07097793-72d8-4e93-a4d3-edb896ce185a", "location": {"lat": 51.504286, "lon": -3.576945}}
    }
class TestFetchUUIDGivenID:

    @patch('data_tree_builder.load_from_json', side_effect=mock_bus_stop_content)
    def test_fetch_UUID(self, mock_method):  # note the added mock_method parameter
        legacy_id = 14668
        JSON_bus_stop_path = "mock_path.json"
        expected_name = "Birmingham"
        expected_uuid = "5415b966-f8b8-4b27-8620-1641c1a43e45"
        actual_name, actual_uuid = data_tree_builder.fetch_name_and_UUID_given_legacy_ID_from_JSON(legacy_id, JSON_bus_stop_path)
        
        assert actual_name == expected_name, f"Expected {expected_name}, but got {actual_name}"
        assert actual_uuid == expected_uuid, f"Expected {expected_uuid}, but got {actual_uuid}"

        # Assert that our mock was called with the correct path
        mock_method.assert_called_once_with(JSON_bus_stop_path)
        
# Test for reachable_URL_call(uuid, limit=100)
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
        actual_url = data_tree_builder.reachable_URL_call(input_uuid)
        
        # Assert that the expected URL matches the actual URL
        assert expected_url == actual_url, f"Expected URL: {expected_url}, but got: {actual_url}"
        
    def test_standard_UUID(self):
        input = "6f51bf86-01a6-423d-ac31-e35277829e91"
        limit = 100
        output = "https://global.api.flixbus.com/cms/cities/6f51bf86-01a6-423d-ac31-e35277829e91/reachable?language=en-gl&country=GB&limit=100"
        assert output == data_tree_builder.reachable_URL_call(input, limit)

    def test_invalid_UUID_format(self):
        with pytest.raises(ValueError):
            data_tree_builder.reachable_URL_call("abcd-1234-efgh")

    def test_empty_UUID(self):
        with pytest.raises(ValueError):
            data_tree_builder.reachable_URL_call("")

    def test_special_char_UUID(self):
        with pytest.raises(ValueError):
            data_tree_builder.reachable_URL_call("1234-5678-9abc-def$")

    def test_case_sensitivity(self):
        input_lower = "a1b2c3d4-e5f6-7a8b-9c0d-ef1234567890"
        input_upper = "A1B2C3D4-E5F6-7A8B-9C0D-EF1234567890"
        limit = 100
        output = "https://global.api.flixbus.com/cms/cities/a1b2c3d4-e5f6-7a8b-9c0d-ef1234567890/reachable?language=en-gl&country=GB&limit=100"
        assert output == data_tree_builder.reachable_URL_call(input_lower, limit)
        assert output == data_tree_builder.reachable_URL_call(input_upper, limit)

    def test_non_integer_limit(self):
        input = "6f51bf86-01a6-423d-ac31-e35277829e91"
        with pytest.raises(ValueError):
            data_tree_builder.reachable_URL_call(input, "forty")

    def test_float_limit(self):
        input = "6f51bf86-01a6-423d-ac31-e35277829e91"
        with pytest.raises(ValueError):
            data_tree_builder.reachable_URL_call(input, 40.5)

    def test_negative_limit(self):
        input = "6f51bf86-01a6-423d-ac31-e35277829e91"
        with pytest.raises(ValueError):
            data_tree_builder.reachable_URL_call(input, -10)

    def test_no_limit(self):
        input = "6f51bf86-01a6-423d-ac31-e35277829e91"
        output = "https://global.api.flixbus.com/cms/cities/6f51bf86-01a6-423d-ac31-e35277829e91/reachable?language=en-gl&country=GB&limit=100"  # Assuming 40 is the default limit
        assert output == data_tree_builder.reachable_URL_call(input)

    def test_large_limit(self):
        input_uuid = "6f51bf86-01a6-423d-ac31-e35277829e91"
        limit = 1000000000
        with pytest.raises(ValueError):
            data_tree_builder.reachable_URL_call(input_uuid, limit)

# Test for fetch_global_api(url: str) -> dict
class TestFetchGlobalApi:
    @patch('requests.get')
    def test_successful_response(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'test_key': 'test_value'}
        mock_get.return_value = mock_response

        url = 'https://example.com/api'
        response_data = data_tree_builder.fetch_global_api(url)

        assert response_data == {'test_key': 'test_value'}

    @patch('requests.get')
    def test_failed_response(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        url = 'https://example.com/api'
        with pytest.raises(Exception):
            data_tree_builder.fetch_global_api(url)

# Test for give_reachable_cities(json_data, legacy_id)          
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
        assert expected == data_tree_builder.give_reachable_cities(json_data)
    

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
        assert expected == data_tree_builder.give_reachable_cities(json_data)   
        
        
def mock_bus_stops_json(dummy_json_path):
    mock_json = {
        "117593": {"name": "Hayle", "id": "110a6a55-6a2f-4fc6-8049-97fa18a59223", "location": {"lat": 50.185467, "lon": -5.42091}},
        "47891": {"name": "Heathrow Airport", "id": "3ed3bb14-b327-4fd8-8a12-465b08ae886d", "location": {"lat": 51.4700223, "lon": -0.4542955}},
        "44201": {"name": "Lancaster", "id": "e6da4098-043b-44e9-9a1c-6fd0b3dd9dac", "location": {"lat": 54.046575, "lon": -2.8007399}}}
    return mock_json
def mock_fetch_reachable_data(uuid, limit = 100):
        # Get the directory of the current script
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the JSON file
        JSON_PATH = os.path.join(BASE_DIR, "hayle_nearby.json")
        # Read the data from the JSON file
        with open(JSON_PATH, 'r') as file:
            json_data = json.load(file)
        return json_data

# Test for city_neighbours_entry(JSON_bus_stop_path, legacy_id_param, is_test_mode=False)
class TestCreateFlixbusDatatree:
    @patch('data_tree_builder.load_from_json', side_effect=mock_bus_stops_json)
    @patch('data_tree_builder.fetch_global_api', side_effect=mock_fetch_reachable_data)
    def test_create_flixbus_datatree(self, mock_bus_stops_json, mock_fetch_reachable_data):
        expected_datatree = {
        "117593": {
            "name": "Hayle",
            "uuid": "110a6a55-6a2f-4fc6-8049-97fa18a59223",
            "neighbors": {
                    "London": "40dfdfd8-8646-11e6-9066-549f350fcb0c",
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
            }
        }
        dummy_json_path = 'mock_path.json'
        result_datatree = data_tree_builder.city_neighbours_entry(dummy_json_path, 117593, is_test_mode=True)
        assert result_datatree == expected_datatree

# Test for _difference_between_dictionaries(old_dict, new_dict)
class TestContradictingNeighbours:
    def test_contradicting_neighbours(self):
        old_dict = {
                    "London": "40dfdfd8-8646-11e6-9066-549f350fcb0c",
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
        new_dict = {
                    "London": "40dfdfd8-8646-11e6-9066-549f350fcb0c",
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
                    "Leeds": "52e0bf1d-25e5-49d0-888e-da8fbc0a25b5"
                }
        expected_result = {
            "removed_entries": {
                "Taunton": "012b776f-8b2a-4ff8-bf22-ff2a90f8a049",
                "Newquay": "6c851f9e-cb08-4f7e-a0ac-9e83a9990045"
            },
            "new_entries": {
                "Leeds": "52e0bf1d-25e5-49d0-888e-da8fbc0a25b5"
            }
        }
        result = data_tree_builder._difference_between_dictionaries(old_dict, new_dict)
        
        assert set(result["removed_entries"].keys()) == set(expected_result["removed_entries"].keys())
        assert set(result["new_entries"].keys()) == set(expected_result["new_entries"].keys())
        
        # Additionally, to check that the associated values are correct:
        for key in result["removed_entries"]:
            assert result["removed_entries"][key] == expected_result["removed_entries"][key]
            
        for key in result["new_entries"]:
            assert result["new_entries"][key] == expected_result["new_entries"][key]

# Test for append_to_json(datatree, filename)
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
        
    def test_append_with_legacy_id(self, temp_json_file):
        self._write_initial_data({
            "117593": {"name": "citya", "id": "UUID_A", "neighbors": {}}
        }, temp_json_file)

        # Data to append
        datatree = {"47891": {"name": "CityB", "neighbors": {"44201": "e6da4098-043b-44e9-9a1c-6fd0b3dd9dac"}}}
        
        data_tree_builder.append_to_json(datatree, temp_json_file)
        updated_data = self._read_data(temp_json_file)
        
        assert updated_data["117593"] == {"name": "citya", "id": "UUID_A", "neighbors": {}}
        assert updated_data["47891"] == {"name": "CityB", "neighbors": {"44201": "e6da4098-043b-44e9-9a1c-6fd0b3dd9dac"}}

    def test_conflicting_city(self, temp_json_file):
        # Initial data setup
        self._write_initial_data({
            "117593": {"name": "citya", "id": "UUID_A", "neighbors": {"CityD": "UUID_D"}}
        }, temp_json_file)

        # Data with conflicting information
        datatree = {"117593" : {"name": "CITYA_NEW", "id": "UUID_A", "neighbors": {"CityD": "UUID_D"}}}

        # Attempt to append
        data_tree_builder.append_to_json(datatree, temp_json_file)

        # Retrieve the updated data
        updated_data = self._read_data(temp_json_file)

        # Check the assertions
        assert "117593" in updated_data
        assert updated_data["117593"]["name"] == "citya"  # Ensure the name remains unchanged
        assert updated_data["117593"]["id"] == "UUID_A"
        assert updated_data["117593"]["neighbors"]["CityD"] == "UUID_D"
    
    def test_different_neighbors(self, temp_json_file):
        # Initial data setup
        self._write_initial_data({
            "117593": {"name": "citya", "id": "UUID_A", "neighbors": {"CityD": "UUID_D"}}
        }, temp_json_file)

        # Data with different neighbors
        datatree = {"117593" : {"name": "citya", "id": "UUID_A", "neighbors": {"CityE": "UUID_E"}}}

        # Attempt to append and catch the exception
        with pytest.raises(Exception) as e_info:
            data_tree_builder.append_to_json(datatree, temp_json_file)

        # Ensure the raised exception has the correct message about the difference in neighbors
        assert "Changes detected in neighbors for city ID 117593." in str(e_info.value)
        assert "Removed: {'CityD': 'UUID_D'}" in str(e_info.value)
        assert "Added: {'CityE': 'UUID_E'}" in str(e_info.value)

        # Retrieve the updated data
        updated_data = self._read_data(temp_json_file)

        # Check that the original data remains unchanged due to the detected difference
        assert "117593" in updated_data
        assert updated_data["117593"]["name"] == "citya"
        assert updated_data["117593"]["id"] == "UUID_A"
        assert updated_data["117593"]["neighbors"]["CityD"] == "UUID_D"
    
    
    def test_appending_to_empty_file(self, temp_json_file):
        self._write_initial_data({}, temp_json_file)
        
        datatree = {"CityE": {"name": "CityE", "uuid": "UUID_E", "neighbors": {}}}
        data_tree_builder.append_to_json(datatree, temp_json_file)
        updated_data = self._read_data(temp_json_file)

        assert updated_data["CityE"] == {"name": "CityE", "uuid": "UUID_E", "neighbors": {}}

    def test_appending_empty_data(self, temp_json_file):
        self._write_initial_data({
            "CityK": {"name": "CityK", "uuid": "UUID_K", "neighbors": {}}
        }, temp_json_file)

        data_tree_builder.append_to_json({}, temp_json_file)
        updated_data = self._read_data(temp_json_file)

        assert updated_data["CityK"] == {"name": "CityK", "uuid": "UUID_K", "neighbors": {}}
    






