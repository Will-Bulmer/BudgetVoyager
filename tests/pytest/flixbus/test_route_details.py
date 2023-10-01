import requests
import pytest
from unittest.mock import patch, Mock
import json
import os
import route_details

class TestFetchGlobalApi:
    @patch('requests.get')
    def test_successful_response(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'test_key': 'test_value'}
        mock_get.return_value = mock_response

        url = 'https://example.com/api'
        response_data = route_details.fetch_global_api(url)

        assert response_data == {'test_key': 'test_value'}

    @patch('requests.get')
    def test_failed_response(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        url = 'https://example.com/api'
        with pytest.raises(Exception):
            route_details.fetch_global_api(url)

class TestIsValidDate:
    def test_is_valid_date(self):
    # Positive test cases
        assert route_details.is_valid_date("29.02.2020") == True, "Failed on case 29.02.2020"
        assert route_details.is_valid_date("28.02.2021") == True, "Failed on case 28.02.2021"
        assert route_details.is_valid_date("31.01.2022") == True, "Failed on case 31.01.2022"
        assert route_details.is_valid_date("15.05.2022") == True, "Failed on case 15.05.2022"
        
        # Negative test cases
        assert route_details.is_valid_date("31.02.2020") == False, "Failed on case 31.02.2020"
        assert route_details.is_valid_date("32.01.2020") == False, "Failed on case 32.01.2020"
        assert route_details.is_valid_date("29.02.2019") == False, "Failed on case 29.02.2019"
        assert route_details.is_valid_date("00.01.2020") == False, "Failed on case 00.01.2020"
        assert route_details.is_valid_date("31.04.2021") == False, "Failed on case 31.04.2021"
        assert route_details.is_valid_date("30.02.2022") == False, "Failed on case 30.02.2022"
        assert route_details.is_valid_date("01.13.2022") == False, "Failed on case 01.13.2022"
        assert route_details.is_valid_date("01.00.2022") == False, "Failed on case 01.00.2022"
        assert route_details.is_valid_date("1.01.2022")  == False, "Failed on case 1.01.2022"
        assert route_details.is_valid_date("01.1.2022")  == False, "Failed on case 01.1.2022"
        assert route_details.is_valid_date("01.01.22")   == False, "Failed on case 01.01.22"
        assert route_details.is_valid_date("29022020")   == False, "Failed on case 29022020"
            
class TestURLCall:

    @staticmethod
    def _check_value_error(func, *args):
        with pytest.raises(ValueError):
            func(*args)

    def test_correct_url_given_uuids(self):
        UUID_FROM = "37270b23-e4a9-45e3-92a6-06bd94ed417b" # Exeter
        UUID_TO = "8aa5378a-5f22-429c-88f7-2468ffab2757" # Bristol
        departure_date = "12.09.2023"
        expected_result = (
            f"https://global.api.flixbus.com/search/service/v4/search?"
            f"from_city_id=37270b23-e4a9-45e3-92a6-06bd94ed417b&"
            f"to_city_id=8aa5378a-5f22-429c-88f7-2468ffab2757&"
            f"departure_date=12.09.2023&"
            f"products=%7B%22adult%22%3A1%7D&"
            f"currency=GBP&"
            f"locale=en_GB&"
            f"search_by=cities&"
            f"include_after_midnight_rides=1"
        )
        assert route_details.route_details_URL_call(UUID_FROM, UUID_TO, departure_date) == expected_result
            
    @pytest.mark.parametrize(
        "UUID_FROM, UUID_TO, departure_date, test_description",
        [
            ("abcd-1234-efgh", "8aa5378a-5f22-429c-88f7-2468ffab", "12.09.2023", "Invalid UUID format for 'from' city"),  # Testing invalid UUID format for 'from' city
            ("37270b23-e4a9-45e3-92a6-06bd94ed417b", "abcd-1234-efgh", "12.09.2023", "Invalid UUID format for 'to' city"),  # Testing invalid UUID format for 'to' city
            ("", "8aa5378a-5f22-429c-88f7-2468ffab", "12.09.2023", "Empty UUID for 'from' city"),  # Testing empty UUID for 'from' city
            ("37270b23-e4a9-45e3-92a6-06bd94ed417b", "", "12.09.2023", "Empty UUID for 'to' city"),  # Testing empty UUID for 'to' city
            ("1234-5678-9abc-def$", "8aa5378a-5f22-429c-88f7-2468ffab", "12.09.2023", "Special character in UUID for 'from' city"),  # Testing special character in UUID for 'from' city
            ("37270b23-e4a9-45e3-92a6-06bd94ed417b", "1234-5678-9abc-def$", "12.09.2023", "Special character in UUID for 'to' city"),  # Testing special character in UUID for 'to' city
            ("37270b23-e4a9-45e3-92a6-06bd94ed417b", "8aa5378a-5f22-429c-88f7-2468ffab", "35.09.2023", "Invalid departure date"),  # Testing invalid departure date format
            ("37270b23-e4a9-45e3-92a6-06bd94ed417b", "8aa5378a-5f22-429c-88f7-2468ffab", "", "Empty departure date")  # Testing empty departure date
        ]
    )
    def test_value_errors(self, UUID_FROM, UUID_TO, departure_date, test_description):
        TestURLCall._check_value_error(route_details.route_details_URL_call, UUID_FROM, UUID_TO, departure_date)
 
class TestConvertNameToUUID:
        def _assert_raises_value_error(self, func, expected_message, *args):
            try:
                func(*args)
                assert False, f"Expected a ValueError with message: {expected_message}"
            except ValueError as e:
                assert str(e) == expected_message, f"Expected message '{expected_message}' but got '{str(e)}'"
    
        def test_standard_responses_and_edge_cases(self):
            example_JSON = {
                "60151": {"name": "Aberdeen", "id": "4588b4ab-79ea-4c6d-88ae-30b58611f263", "location": {"lat": 57.149717, "lon": -2.094278}},
                "51081": {"name": "Amesbury", "id": "ce39aa68-df35-4462-a239-1edd92241574", "location": {"lat": 51.1679201, "lon": -1.7629783}},
                "14668": {"name": "Birmingham", "id": "5415b966-f8b8-4b27-8620-1641c1a43e45", "location": {"lat": 52.4829, "lon": -1.8936}}
            }
            input_name = "Aberdeen"
            expected_output = "4588b4ab-79ea-4c6d-88ae-30b58611f263"
            
            # 0. Standard Response
            assert route_details.convert_name_to_uuid(input_name, example_JSON) == expected_output
            
            # 1. City Name Not Present
            self._assert_raises_value_error(route_details.convert_name_to_uuid, "'NotPresentCity' not found in the provided JSON.", "NotPresentCity", example_JSON)

            # 2. Empty City Name
            self._assert_raises_value_error(route_details.convert_name_to_uuid, "'' not found in the provided JSON.", "", example_JSON)

            # 3. Non-string Input for City Name
            self._assert_raises_value_error(route_details.convert_name_to_uuid, "'1234' not found in the provided JSON.", 1234, example_JSON)

            # 4. Empty JSON
            self._assert_raises_value_error(route_details.convert_name_to_uuid, "'Aberdeen' not found in the provided JSON.", "Aberdeen", {})

            # 5. City Name Case Sensitivity
            self._assert_raises_value_error(route_details.convert_name_to_uuid, "'ABERDEEN' not found in the provided JSON.", "ABERDEEN", example_JSON)
            
class TestRouteDetailsExtraction :
    def _load_from_json(self,file_path: str) -> dict:
        with open(file_path, 'r') as file:
            return json.load(file)
        
    def test_standard_reponse_Amesbury_to_London(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        JSON_example_path = os.path.join(BASE_DIR, "route1_example.json")
        
        example_data = self._load_from_json(JSON_example_path)
        expected_output = [("Amesbury", "2023-10-02T08:55:00+01:00", "London Hammersmith Bus Station (Bay D)", "2023-10-02T10:45:00+01:00", 20, 5, "flixbus")]

        assert route_details.extract_route_details_from_json(example_data) == expected_output   
        
    def test_standard_response_Bristol_to_London(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        JSON_example_path = os.path.join(BASE_DIR, "route2_example.json")

        example_data = self._load_from_json(JSON_example_path)
        expected_output = [("Bristol (Bond Street North)", "2023-10-02T03:00:00+01:00", "London Hammersmith", "2023-10-02T05:50:00+01:00", 5.99, 15, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T03:00:00+01:00", "London Victoria Coach Station", "2023-10-02T06:10:00+01:00", 4.99, 15, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T07:00:00+01:00", "London Hammersmith", "2023-10-02T09:20:00+01:00", 7.99, 14, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T07:00:00+01:00", "London Victoria Coach Station", "2023-10-02T09:50:00+01:00", 7.99, 14, "flixbus"),
                        ("Bristol Uni of West England", "2023-10-02T07:10:00+01:00", "London Hammersmith", "2023-10-02T09:20:00+01:00", 7.99, 14, "flixbus"),
                        ("Bristol Uni of West England", "2023-10-02T07:10:00+01:00", "London Victoria Coach Station", "2023-10-02T09:50:00+01:00", 7.99, 14, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T10:30:00+01:00", "London Hammersmith", "2023-10-02T12:55:00+01:00", 19.99, 6, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T10:30:00+01:00", "London Victoria Coach Station", "2023-10-02T13:25:00+01:00", 19.99, 6, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T11:30:00+01:00", "London Hammersmith", "2023-10-02T14:00:00+01:00", 9.99, 14, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T11:30:00+01:00", "London Victoria Coach Station", "2023-10-02T14:30:00+01:00", 9.99, 14, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T15:00:00+01:00", "London Hammersmith", "2023-10-02T17:20:00+01:00", 7.99, 20, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T15:00:00+01:00", "London Victoria Coach Station", "2023-10-02T17:50:00+01:00", 7.99, 20, "flixbus"),
                        ("Bristol Uni of West England", "2023-10-02T15:10:00+01:00", "London Hammersmith", "2023-10-02T17:20:00+01:00", 7.99, 20, "flixbus"),
                        ("Bristol Uni of West England", "2023-10-02T15:10:00+01:00", "London Victoria Coach Station", "2023-10-02T17:50:00+01:00", 7.99, 20, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T18:40:00+01:00", "London Hammersmith", "2023-10-02T21:05:00+01:00", 13.99, 10, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T18:40:00+01:00", "London Victoria Coach Station", "2023-10-02T21:30:00+01:00", 13.99, 10, "flixbus")]
                            
        
        assert route_details.extract_route_details_from_json(example_data) == expected_output 
        
class TestBehaviouralRouteDetails:
    @patch("route_details.fetch_global_api")
    def test_standard_response_amesbury_to_london(self, mock_fetch):
        # 1. Mock the fetch_global_api to return route1_example.json content
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        JSON_example_path = os.path.join(BASE_DIR, "route1_example.json")
        with open(JSON_example_path, "r") as file:
            mock_route_data = json.load(file)
        mock_fetch.return_value = mock_route_data

        # 4. Actual Test
        input_departure = "Amesbury"
        input_arrival = "London"
        input_date = "02.10.2023"
        expected_output = [("Amesbury", "2023-10-02T08:55:00+01:00", "London Hammersmith Bus Station (Bay D)", "2023-10-02T10:45:00+01:00", 20, 5, "flixbus")]
        
        mock_json_data_path = "bus_stops.json" 
        result = route_details.extract_journey_info(input_departure, input_arrival, input_date, mock_json_data_path)
        assert result == expected_output
        
    @patch("route_details.fetch_global_api")        
    def test_standard_response_bristol_to_london(self, mock_fetch):
        # 1. Mock the fetch_global_api to return route1_example.json content
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        JSON_example_path = os.path.join(BASE_DIR, "route2_example.json")
        with open(JSON_example_path, "r") as file:
            mock_route_data = json.load(file)
        mock_fetch.return_value = mock_route_data

        # 4. Actual Test
        input_departure = "Bristol"
        input_arrival = "London"
        input_date = "02.10.2023"
        expected_output = [("Bristol (Bond Street North)", "2023-10-02T03:00:00+01:00", "London Hammersmith", "2023-10-02T05:50:00+01:00", 5.99, 15, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T03:00:00+01:00", "London Victoria Coach Station", "2023-10-02T06:10:00+01:00", 4.99, 15, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T07:00:00+01:00", "London Hammersmith", "2023-10-02T09:20:00+01:00", 7.99, 14, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T07:00:00+01:00", "London Victoria Coach Station", "2023-10-02T09:50:00+01:00", 7.99, 14, "flixbus"),
                        ("Bristol Uni of West England", "2023-10-02T07:10:00+01:00", "London Hammersmith", "2023-10-02T09:20:00+01:00", 7.99, 14, "flixbus"),
                        ("Bristol Uni of West England", "2023-10-02T07:10:00+01:00", "London Victoria Coach Station", "2023-10-02T09:50:00+01:00", 7.99, 14, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T10:30:00+01:00", "London Hammersmith", "2023-10-02T12:55:00+01:00", 19.99, 6, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T10:30:00+01:00", "London Victoria Coach Station", "2023-10-02T13:25:00+01:00", 19.99, 6, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T11:30:00+01:00", "London Hammersmith", "2023-10-02T14:00:00+01:00", 9.99, 14, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T11:30:00+01:00", "London Victoria Coach Station", "2023-10-02T14:30:00+01:00", 9.99, 14, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T15:00:00+01:00", "London Hammersmith", "2023-10-02T17:20:00+01:00", 7.99, 20, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T15:00:00+01:00", "London Victoria Coach Station", "2023-10-02T17:50:00+01:00", 7.99, 20, "flixbus"),
                        ("Bristol Uni of West England", "2023-10-02T15:10:00+01:00", "London Hammersmith", "2023-10-02T17:20:00+01:00", 7.99, 20, "flixbus"),
                        ("Bristol Uni of West England", "2023-10-02T15:10:00+01:00", "London Victoria Coach Station", "2023-10-02T17:50:00+01:00", 7.99, 20, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T18:40:00+01:00", "London Hammersmith", "2023-10-02T21:05:00+01:00", 13.99, 10, "flixbus"),
                        ("Bristol (Bond Street North)", "2023-10-02T18:40:00+01:00", "London Victoria Coach Station", "2023-10-02T21:30:00+01:00", 13.99, 10, "flixbus")]
        
        mock_json_data_path = "bus_stops.json" 
        result = route_details.extract_journey_info(input_departure, input_arrival, input_date, mock_json_data_path)
        assert result == expected_output
        
        