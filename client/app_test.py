# app_test.py
import unittest
from unittest.mock import patch, MagicMock
import requests
import app  # assuming your script is saved as client.py

class TestDNSClient(unittest.TestCase):

    @patch('builtins.input', side_effect=['example.com', 'exit'])
    @patch('requests.get')
    def test_successful_resolution(self, mock_get, mock_input):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'ip': '192.168.1.10'}
        mock_get.return_value = mock_response

        with patch('builtins.print') as mock_print:
            app.main()

        mock_get.assert_called_with(
            'http://localhost:8001/resolve', params={'domain': 'example.com'}, timeout=5
        )
        mock_print.assert_any_call("Resolved IP: 192.168.1.10")
        mock_print.assert_any_call("Exiting client.")

    @patch('builtins.input', side_effect=['test.com', 'exit'])
    @patch('requests.get')
    def test_domain_not_found(self, mock_get, mock_input):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'error': "Domain 'test.com' not found"}
        mock_get.return_value = mock_response

        with patch('builtins.print') as mock_print:
            app.main()

        mock_print.assert_any_call("Error: Domain 'test.com' not found")

    @patch('builtins.input', side_effect=['', 'exit'])
    @patch('requests.get')
    def test_empty_input(self, mock_get, mock_input):
        with patch('builtins.print') as mock_print:
            app.main()

        # Should skip requests.get due to empty input
        mock_get.assert_not_called()
        mock_print.assert_any_call("Exiting client.")

    @patch('builtins.input', side_effect=['example.com', 'exit'])
    @patch('requests.get', side_effect=requests.exceptions.ConnectionError("Connection failed"))
    def test_request_exception(self, mock_get, mock_input):
        with patch('builtins.print') as mock_print:
            app.main()

        mock_print.assert_any_call("Request failed: Connection failed")
        mock_print.assert_any_call("Exiting client.")

if __name__ == '__main__':
    unittest.main()
