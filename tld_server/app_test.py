# app_test.py
import unittest
from unittest.mock import patch, MagicMock
import json
import requests
from app import app

class TestRecursiveDNSResolver(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    @patch('requests.get')
    def test_successful_resolution_com(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'ip': '192.168.1.10'}
        mock_get.return_value = mock_response

        response = self.client.get('/resolve?domain=example.com')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['ip'], '192.168.1.10')

        mock_get.assert_called_with(
            'http://localhost:8002/resolve',
            params={'domain': 'example.com'},
            timeout=5
        )

    def test_invalid_domain(self):
        response = self.client.get('/resolve?domain=invalid-domain')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Invalid domain')

    def test_missing_domain_param(self):
        response = self.client.get('/resolve')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Invalid domain')

    def test_unsupported_tld(self):
        response = self.client.get('/resolve?domain=example.xyz')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], "TLD 'xyz' not supported")

    @patch('requests.get', side_effect=requests.exceptions.ConnectionError("Server down"))
    def test_upstream_server_failure(self, mock_get):
        response = self.client.get('/resolve?domain=example.com')
        self.assertEqual(response.status_code, 502)
        data = json.loads(response.data)
        self.assertIn("Failed to contact authoritative server", data['error'])

if __name__ == '__main__':
    unittest.main()
