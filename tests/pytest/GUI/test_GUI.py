import pytest
import json
import os
from unittest.mock import MagicMock
from unittest.mock import patch, Mock, mock_open
from GUI import JSONBackend  # Adjust the import to your actual module name

class TestJSONBackend:

    @pytest.fixture(scope="function")
    def backend(self):
        return JSONBackend()

    def test_jsonData_property(self, backend):
        test_data = '{"test": "data"}'
        backend._jsonData = test_data
        assert backend.jsonData == test_data
        
    @patch("os.path.exists", return_value=False)
    @patch.object(JSONBackend, "jsonLoadError")
    def test_loadJSON_file_not_exists(self, mock_jsonLoadError, mock_exists, backend):
        fake_path = "non_existent.json"
        backend.loadJSON(fake_path)
        mock_jsonLoadError.emit.assert_called_with("File does not exist")

    @pytest.mark.parametrize(
        "content,expected_output,expected_signal", 
        [
            ('{"key": "value"}', '{"key": "value"}', "jsonLoaded"), 
            ("{ this is : invalid json }", None, "jsonLoadError")
        ]
    )
    def test_loadJSON_file_handling(self, backend, mocker, content, expected_output, expected_signal):
        fake_path = "some_file.json"
        m = mock_open(read_data=content)
        mocker.patch("builtins.open", m)

        # Mocking os.path.exists to always return True
        mocker.patch("os.path.exists", return_value=True)

        mock_jsonLoaded = mocker.patch.object(backend, 'jsonLoaded')
        mock_jsonLoadError = mocker.patch.object(backend, 'jsonLoadError')

        backend.loadJSON(fake_path)

        if expected_signal == "jsonLoaded":
            mock_jsonLoaded.emit.assert_called_with(expected_output)
        else:
            mock_jsonLoadError.emit.assert_called()


    # You can extend the test cases further by adding more scenarios to the parametrize list or more tests.
