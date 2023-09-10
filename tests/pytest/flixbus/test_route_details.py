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