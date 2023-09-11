import pytest
import json
from unittest.mock import patch, Mock
import unittest
import api_utils

# Test for create_fetch_name_and_UUID_URL(legacy_id)
class TestCreateFetchNameAndUUIDURL:
    def setup_method(self):
        self.function_to_test = api_utils.create_fetch_name_and_UUID_URL
        self.expected_url_base = "https://global.api.flixbus.com/search/service/cities/details?locale=en_GB&from_city_id="

    def test_returns_correct_url_for_valid_id(self):
        legacy_id = 12345
        expected_url = f"{self.expected_url_base}{legacy_id}"
        result = self.function_to_test(legacy_id)
        assert result == expected_url, f"Expected {expected_url} but got {result}"

    @pytest.mark.parametrize('invalid_id', [123.45, "12345", "abcde", -12345, None])
    def test_invalid_id_raises_error(self, invalid_id):
        with pytest.raises(ValueError, match="legacy_id must be a positive integer."):
            self.function_to_test(invalid_id)

# Test for fetch_global_api(url: str) -> dict
class TestFetchGlobalApi:
    def setup_method(self):
        self.url = 'https://example.com/api'
        self.function_to_test = api_utils.fetch_global_api

    @patch('requests.get')
    def test_returns_data_for_successful_response(self, mock_get):
        # Setup mock to return a successful response
        mock_response = self._mock_response(status_code=200, json_data={'test_key': 'test_value'})
        mock_get.return_value = mock_response

        # Call the function and verify the result
        response_data = self.function_to_test(self.url)
        assert response_data == {'test_key': 'test_value'}

    @patch('requests.get')
    def test_raises_exception_for_failed_response(self, mock_get):
        # Setup mock to return a 404
        mock_response = self._mock_response(status_code=404)
        mock_get.return_value = mock_response

        # Expect an exception when the function is called
        with pytest.raises(Exception):
            self.function_to_test(self.url)
            
    def _mock_response(self, status_code=200, json_data=None):
        """Helper to build mock responses."""
        mock_response = Mock()
        mock_response.status_code = status_code
        if json_data:
            mock_response.json.return_value = json_data
        return mock_response

# Test for extract_name_and_UUID(data: dict) -> tuple
class TestExtractNameAndUUID:
    def setup_method(self):
        self.function_to_test = api_utils.extract_name_and_UUID
        
    def test_extract_name_and_UUID_expected(self):
        input_data = [{"id":"52e0bf1d-25e5-49d0-888e-da8fbc0a25b5","legacy_id":43121,"name":"Leeds","country_code":"GB","timezone_offset":3600}]
        expected_output = 43121, "Leeds", "52e0bf1d-25e5-49d0-888e-da8fbc0a25b5"
        self._assert_extraction(input_data, expected_output)
        
    def test_multiple_dictionaries_in_list(self):
        input_data = [
            {"id":"52e0bf1d-25e5-49d0-888e-da8fbc0a25b5","legacy_id":43121,"name":"Leeds","country_code":"GB","timezone_offset":3600},
            {"id":"abcdefg-25e5-49d0-888e-hijklmnopqr","legacy_id":54321,"name":"Manchester","country_code":"GB","timezone_offset":3600}
        ]
        expected_output = 43121, "Leeds", "52e0bf1d-25e5-49d0-888e-da8fbc0a25b5"
        self._assert_extraction(input_data, expected_output)
    
    def test_raises_error_for_empty_list(self):
        self._assert_raises(ValueError, "Data should be a non-empty list of dictionaries.", [])
    def test_missing_keys(self):
        self._assert_raises(ValueError, "Data is missing essential keys.", [{"legacy_id":43121,"country_code":"GB","timezone_offset":3600}])
    def test_non_dictionary_item_in_list(self):
        self._assert_raises(ValueError, "Data is missing essential keys.", ["not a dictionary", 123, 456])
    
    def _assert_extraction(self, input_data, expected_output):
        result = self.function_to_test(input_data)
        assert result == expected_output, f"Expected {expected_output} but got {result}"

    def _assert_raises(self, exception, match_text, input_data):
        with pytest.raises(exception, match=match_text):
            self.function_to_test(input_data)

# Test for append_name_and_UUID(legacy_id, city_name, city_id, file_path)
# In Python, JSON keys are ALWAYS strings
class TestAppendNameAndUUID:
    @pytest.fixture(autouse=True)
    def set_up(self, tmpdir):
        self.JSON_file = tmpdir.join("test_file.json")
        self.function_to_test = api_utils.append_name_and_UUID
        
    def _write_to_JSON_file(self, data):
        """Helper function to write data to JSON file."""
        self.JSON_file.write(json.dumps(data))
        
    def test_append_name_and_UUID_expected(self):
        mock_JSON = {
            "60151": {"name": "name", "id": "code", "location": {"lon": "0.0", "lat": "0.0"}},
            "51081": {"name": "name", "id": "code", "location": {"lon": "0.0", "lat": "0.0"}}
        }
        self._write_to_JSON_file(mock_JSON)
        expected_output = {
            "60151": {"name": "Leeds", "id": "52e0bf1d-25e5-49d0-888e-da8fbc0a25b5", "location": {"lon": "0.0", "lat": "0.0"}},
            "51081": {"name": "name", "id": "code", "location": {"lon": "0.0", "lat": "0.0"}}
        }
        assert expected_output == self.function_to_test(60151, "Leeds", "52e0bf1d-25e5-49d0-888e-da8fbc0a25b5", self.JSON_file)

    def test_append_name_and_UUID_str_ID_input(self):
        mock_JSON = {
            "60151": {"name": "name", "id": "code", "location": {"lon": "0.0", "lat": "0.0"}},
            "51081": {"name": "name", "id": "code", "location": {"lon": "0.0", "lat": "0.0"}}
        }
        self._write_to_JSON_file(mock_JSON)
        expected_output = {
            "60151": {"name": "Leeds", "id": "52e0bf1d-25e5-49d0-888e-da8fbc0a25b5", "location": {"lon": "0.0", "lat": "0.0"}},
            "51081": {"name": "name", "id": "code", "location": {"lon": "0.0", "lat": "0.0"}}
        }
        assert expected_output == self.function_to_test("60151", "Leeds", "52e0bf1d-25e5-49d0-888e-da8fbc0a25b5", self.JSON_file)
    
    def test_append_name_and_UUID_int_ID_JSON(self):
        mock_JSON = {
            60151: {"name": "name", "id": "code", "location": {"lon": "0.0", "lat": "0.0"}},
            51081: {"name": "name", "id": "code", "location": {"lon": "0.0", "lat": "0.0"}}
        }
        self._write_to_JSON_file(mock_JSON)
        expected_output = {
            "60151": {"name": "Leeds", "id": "52e0bf1d-25e5-49d0-888e-da8fbc0a25b5", "location": {"lon": "0.0", "lat": "0.0"}},
            "51081": {"name": "name", "id": "code", "location": {"lon": "0.0", "lat": "0.0"}}
        }
        assert expected_output == self.function_to_test("60151", "Leeds", "52e0bf1d-25e5-49d0-888e-da8fbc0a25b5", self.JSON_file)
        
    def append_name_and_UUID_int_ID_JSON_and_Input(self):
        mock_JSON = {
            60151: {"name": "name", "id": "code", "location": {"lon": "0.0", "lat": "0.0"}},
            51081: {"name": "name", "id": "code", "location": {"lon": "0.0", "lat": "0.0"}}
        }
        self._write_to_JSON_file(mock_JSON)
        expected_output = {
            "60151": {"name": "Leeds", "id": "52e0bf1d-25e5-49d0-888e-da8fbc0a25b5", "location": {"lon": "0.0", "lat": "0.0"}},
            "51081": {"name": "name", "id": "code", "location": {"lon": "0.0", "lat": "0.0"}}
        }
        assert expected_output == self.function_to_test(60151, "Leeds", "52e0bf1d-25e5-49d0-888e-da8fbc0a25b5", self.JSON_file)
        
    def test_missing_key(self):
        mock_JSON = {
            "60151": {"name": "name", "id": "code", "location": {"lon": "0.0", "lat": "0.0"}}
        }
        self._write_to_JSON_file(mock_JSON)
        with pytest.raises(KeyError, match="No entry found for legacy_id: 99999"):
            self.function_to_test(99999, "NotFoundCity", "not-a-real-id", self.JSON_file)

    def test_invalid_data_dict(self):
        mock_JSON = {
            60151: "This is not a valid dictionary structure"
        }
        self._write_to_JSON_file(mock_JSON)
        with pytest.raises(TypeError):
            self.function_to_test(60151, "CityName", "city-id", self.JSON_file)

# Test for create_fetch_name_and_UUID_URL(legacy_id)
class TestCreateFetchNameAndUUIDURL:
    def setup_method(self):
        self.function_to_test = api_utils.create_fetch_location_URL

    def test_returns_correct_url_for_valid_name(self):
        name = "Aberdeen"
        expected_url = f"https://global.api.flixbus.com/search/autocomplete/cities?q=Aberdeen&lang=en&country=gb&flixbus_cities_only=false&stations=false"
        result = self.function_to_test(name)
        assert result == expected_url, f"Expected {expected_url} but got {result}"
    
    def test_returns_correct_url_for_name_with_space(self):
        name = "Heathrow Airport"
        expected_url = f"https://global.api.flixbus.com/search/autocomplete/cities?q=Heathrow-Airport&lang=en&country=gb&flixbus_cities_only=false&stations=false"
        result = self.function_to_test(name)
        assert result == expected_url, f"Expected {expected_url} but got {result}"

    @pytest.mark.parametrize('invalid_name', [123.45, -12345, None])
    def test_invalid_id_raises_error(self, invalid_name):
        with pytest.raises(ValueError, match="name must be a String."):
            self.function_to_test(invalid_name)

# Test for extract_lat_and_lon(data: list) -> tuple
class TestExtractLatAndLon:
    
    def setup_method(self):
        self.function_to_test = api_utils.extract_lat_and_lon
        
    def test_extract_lat_and_lon_expected(self):
        input_data = [
        {
            "score":62.36875,
            "country":"gb",
            "has_train_station":False,
            "district":None,
            "name":"Amesbury",
            "legacy_id":51081,
            "location":{"lat":51.1679201,"lon":-1.7629783},
            "timezone_offset_seconds":3600,
            "id":"ce39aa68-df35-4462-a239-1edd92241574",
            "stations":[],
            "is_flixbus_city":True
        }
        ]
        expected_output = 51.1679201, -1.7629783
        self._assert_extraction(input_data, expected_output, 51081)
    
    def test_multiple_dictionaries_in_list(self):
        input_data = [
            {
                "score":63.1475,
                "country":"gb",
                "has_train_station":False,
                "district":None,
                "name":"Winchester",
                "legacy_id":61092,
                "location":{"lat":51.059771,"lon":-1.310142},
                "timezone_offset_seconds":3600,
                "id":"ae35de47-gh35-3456-a456-2fgh98765432",
                "stations":[],
                "is_flixbus_city":True
            },
            {
                "score":62.36875,
                "country":"gb",
                "has_train_station":False,
                "district":None,
                "name":"Amesbury",
                "legacy_id":51081,
                "location":{"lat":51.1679201,"lon":-1.7629783},
                "timezone_offset_seconds":3600,
                "id":"ce39aa68-df35-4462-a239-1edd92241574",
                "stations":[],
                "is_flixbus_city":True
            }
        ]
        expected_output = 51.1679201, -1.7629783
        self._assert_extraction(input_data, expected_output, 51081)

    @pytest.mark.parametrize(
        "input_data, exception, match_text, legacy_id",
        [
            # Test case for empty list
            ([], ValueError, "Data should be a non-empty list of dictionaries.", 60151),
            # Test case for missing keys
            ([{"legacy_id":43121,"country_code":"GB","timezone_offset":3600}], ValueError, "Data is missing lat or lon.", 43121),
            # Test case for non-dictionary item in list
            (["not a dictionary", 123, 456], ValueError, None, 60151),
        ]
    )
    def test_error_cases(self, input_data, exception, match_text, legacy_id):
        self._assert_raises(exception, match_text, input_data, legacy_id)
    
    def _assert_extraction(self, input_data, expected_output, legacy_id):
        result = self.function_to_test(input_data, legacy_id)
        assert result == expected_output, f"Expected {expected_output} but got {result}"


    def _assert_raises(self, exception, match_text, input_data, legacy_id):
        if match_text:
            with pytest.raises(exception, match=match_text):
                self.function_to_test(input_data, legacy_id)
        else:
            with pytest.raises(exception):
                self.function_to_test(input_data, legacy_id)

# Test for append_lat_and_lon(legacy_id, lat, lon, file_path)
class TestAppendLonAndLat:
    @pytest.fixture(autouse=True)
    def set_up(self, tmpdir):
        self.JSON_file = tmpdir.join("test_file.json")
        self.function_to_test = api_utils.append_lat_and_lon

    def _write_to_JSON_file(self, data):
        """Helper function to write data to JSON file."""
        self.JSON_file.write(json.dumps(data))

    def test_append_lon_and_lat_expected(self):
        mock_JSON = {
            "60151": {"name": "name1", "id": "code", "location": {"lat": "0.0", "lon": "0.0"}},
            "51081": {"name": "name2", "id": "code", "location": {"lat": "0.0", "lon": "0.0"}}
        }
        self._write_to_JSON_file(mock_JSON)
        expected_output = {
            "60151": {"name": "name1", "id": "code", "location": {"lat": 51.1679201, "lon": -1.7629783}},
            "51081": {"name": "name2", "id": "code", "location": {"lat": "0.0", "lon": "0.0"}}
        }
        assert expected_output == self.function_to_test(60151, 51.1679201, -1.7629783, self.JSON_file)
        
    def test_append_lon_and_lat_str_ID(self):
        mock_JSON = {
            "60151": {"name": "name1", "id": "code", "location": {"lat": "0.0", "lon": "0.0"}},
            "51081": {"name": "name2", "id": "code", "location": {"lat": "0.0", "lon": "0.0"}}
        }
        self._write_to_JSON_file(mock_JSON)
        expected_output = {
            "60151": {"name": "name1", "id": "code", "location": {"lat": 51.1679201, "lon": -1.7629783}},
            "51081": {"name": "name2", "id": "code", "location": {"lat": "0.0", "lon": "0.0"}}
        }
        assert expected_output == self.function_to_test("60151", 51.1679201, -1.7629783, self.JSON_file)
        
    def test_append_lon_and_lat_int_JSON(self):
        mock_JSON = {
            60151: {"name": "name1", "id": "code", "location": {"lat": "0.0", "lon": "0.0"}},
            51081: {"name": "name2", "id": "code", "location": {"lat": "0.0", "lon": "0.0"}}
        }
        self._write_to_JSON_file(mock_JSON)
        expected_output = {
            "60151": {"name": "name1", "id": "code", "location": {"lat": 51.1679201, "lon": -1.7629783}},
            "51081": {"name": "name2", "id": "code", "location": {"lat": "0.0", "lon": "0.0"}}
        }
        assert expected_output == self.function_to_test("60151", 51.1679201, -1.7629783, self.JSON_file)
        
    def test_append_lon_and_lat_int_ID_Input_and_JSON(self):
        mock_JSON = {
            60151: {"name": "name1", "id": "code", "location": {"lat": "0.0", "lon": "0.0"}},
            51081: {"name": "name2", "id": "code", "location": {"lat": "0.0", "lon": "0.0"}}
        }
        self._write_to_JSON_file(mock_JSON)
        expected_output = {
            "60151": {"name": "name1", "id": "code", "location": {"lat": 51.1679201, "lon": -1.7629783}},
            "51081": {"name": "name2", "id": "code", "location": {"lat": "0.0", "lon": "0.0"}}
        }
        assert expected_output == self.function_to_test(60151, 51.1679201, -1.7629783, self.JSON_file)

    def test_missing_key(self):
        mock_JSON = {
            "60151": {"name": "name", "id": "code", "location": {"lat": "0.0", "lon": "0.0"}}
        }
        self._write_to_JSON_file(mock_JSON)
        with pytest.raises(KeyError, match="No entry found for legacy_id: 99999"):
            self.function_to_test(99999, 51.1679201, -1.7629783, self.JSON_file)

    def test_invalid_data_dict(self):
        mock_JSON = {
            60151: "This is not a valid dictionary structure"
        }
        self._write_to_JSON_file(mock_JSON)
        with pytest.raises(TypeError):
            self.function_to_test(60151, 51.1679201, -1.7629783, self.JSON_file)


def mock_name_and_UUID_response(url):
    return [{"id":"4588b4ab-79ea-4c6d-88ae-30b58611f263","legacy_id":60151,"name":"Aberdeen","country_code":"GB","timezone_offset":3600}]
def mock_lat_and_lon_response(fetched_data):
    return [
        {
            "score": 60.233643,
            "country": "gb",
            "has_train_station": False,
            "district": None,
            "name": "Aberdeen",
            "legacy_id": 60151,
            "location": {
                "lon": -2.094278,
                "lat": 57.149717
            },
            "timezone_offset_seconds": 3600,
            "id": "4588b4ab-79ea-4c6d-88ae-30b58611f263",
            "stations": [],
            "is_flixbus_city": True
        },
        {
            "score": 52.443455,
            "country": "us",
            "has_train_station": False,
            "district": None,
            "name": "Aberdeen, MD",
            "legacy_id": 68243,
            "location": {
                "lon": -76.1641197,
                "lat": 39.5095556
            },
            "timezone_offset_seconds": -14400,
            "id": "f9aacfc5-0dd6-45fb-a8fc-8be35201d577",
            "stations": [],
            "is_flixbus_city": True
        },
        {
            "score": 18.025408,
            "country": "us",
            "has_train_station": False,
            "district": None,
            "name": "Aberdeen, SD",
            "legacy_id": 106673,
            "location": {
                "lon": -98.4864829,
                "lat": 45.4646985
            },
            "timezone_offset_seconds": -18000,
            "id": "2aa572a8-0182-4f74-a1af-d56c1600c94b",
            "stations": [],
            "is_flixbus_city": True
        }
    ]
def mock_fetch_global_api(url):
    if "from_city_id" in url:
        return mock_name_and_UUID_response(url)
    elif "q=" in url:
        return mock_lat_and_lon_response(url)
    return []

# Test for update_bus_stops(JSON_file_path, is_test_mode=False)
class TestUpdateBusStops:
    @pytest.fixture(autouse=True)
    def set_up(self, tmpdir):
        self.JSON_file_path = tmpdir.join("test_file.json")
        self.function_to_test = api_utils.update_bus_stops

    def _write_to_JSON_file(self, data):
        """Helper function to write data to JSON file."""
        self.JSON_file_path.write(json.dumps(data))

    def _read_JSON_file(self):
        """Helper function to read data from JSON file."""
        with open(self.JSON_file_path, 'r') as file:
            return json.load(file)

    @patch('api_utils.fetch_global_api', side_effect=mock_fetch_global_api)
    def test_names_updated(self, mock_fetch_global_api):
        mock_JSON = {
            "60151": {"name": "name", "id": "code", "location": {"lon": "0.0", "lat": "0.0"}},
        }
        self.JSON_file_path.write("")
        self._write_to_JSON_file(mock_JSON)
        expected_output = {
            "60151": {"name": "Aberdeen", "id": "4588b4ab-79ea-4c6d-88ae-30b58611f263", "location": {"lat": "0.0", "lon": "0.0"}},
        }
        data = self._read_JSON_file()
        api_utils._update_data(data, self.JSON_file_path, api_utils.url_for_name_and_UUID, api_utils.extract_for_name_and_UUID, api_utils.append_name_and_UUID, is_test_mode = True)

        #api_utils._update_names_and_UUID(data, self.JSON_file_path, is_test_mode = True)
        assert self._read_JSON_file() == expected_output

    @patch('api_utils.fetch_global_api', side_effect=mock_fetch_global_api)
    def test_location_updated(self, mock_fetch_global_api):
        mock_JSON = {
            "60151": {"name": "Aberdeen", "id": "4588b4ab-79ea-4c6d-88ae-30b58611f263", "location": {"lon": "0.0", "lat": "0.0"}},
        }
        self.JSON_file_path.write("")
        self._write_to_JSON_file(mock_JSON)
        expected_output = {
            "60151": {"name": "Aberdeen", "id": "4588b4ab-79ea-4c6d-88ae-30b58611f263", "location": {"lat": 57.149717, "lon": -2.094278}},
        }
        data = self._read_JSON_file()
        api_utils._update_data(data, self.JSON_file_path,  api_utils.url_for_location, api_utils.extract_for_location, api_utils.append_lat_and_lon, is_test_mode = True)
        #api_utils._update_location(data, self.JSON_file_path, is_test_mode = True)
        assert self._read_JSON_file() == expected_output
    
    @patch('api_utils.fetch_global_api', side_effect=mock_fetch_global_api)
    def updates_as_expected(self, mock_fetch_global_api):
        mock_JSON = {
            "60151": {"name": "name", "id": "code", "location": {"lon": "0.0", "lat": "0.0"}},
        }
        self.JSON_file_path.write("")
        self._write_to_JSON_file(mock_JSON)
        expected_output = {
            "60151": {"name": "Aberdeen", "id": "4588b4ab-79ea-4c6d-88ae-30b58611f263", "location": {"lat": 57.149717, "lon": -2.094278}},
        }

        # Call the function with the JSON file path
        self.function_to_test(self.JSON_file_path, is_test_mode=True)
        assert self._read_JSON_file() == expected_output
