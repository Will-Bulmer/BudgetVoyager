import requests
import pytest
from unittest.mock import patch, Mock
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
    
          
class TestsURLCall:

    def _check_value_error(func, *args):
        with pytest.raises(ValueError):
            func(*args)

    def correct_url_given_uuids(self):
        UUID_FROM = "37270b23-e4a9-45e3-92a6-06bd94ed417b" # Exeter
        UUID_TO = "8aa5378a-5f22-429c-88f7-2468ffab" # Bristol
        departure_date = "12.09.2023"
        expected_result = (
            f"https://global.api.flixbus.com/search/service/v4/search?"
            f"from_city_id=37270b23-e4a9-45e3-92a6-06bd94ed417b&"
            f"to_city_id=8aa5378a-5f22-429c-88f7-2468ffab&"
            f"departure_date=12.09.2023&"
            f"products=%7B%22adult%22%3A1%7D&"
            f"currency=GBP&"
            f"locale=en_GB&"
            f"search_by=cities&"
            f"include_after_midnight_rides=1"
        )
        assert route_details.route_details_URL_call(UUID_FROM, UUID_TO, departure_date)
            
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
    def test_value_errors(UUID_FROM, UUID_TO, departure_date, test_description):
        _check_value_error(route_details.route_details_URL_call, UUID_FROM, UUID_TO, departure_date)
 
   