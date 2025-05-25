# app_test.py
import unittest
import json
from app import app

class TestDomainResolver(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        self.client = app.test_client()
        self.client.testing = True

    def test_resolve_known_domain(self):
        # Test a domain that is in DOMAIN_IP_MAP
        response = self.client.get('/resolve?domain=example.com')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('ip', data)
        self.assertEqual(data['ip'], '192.168.1.10')

    def test_resolve_unknown_domain(self):
        # Test a domain that is not in DOMAIN_IP_MAP
        response = self.client.get('/resolve?domain=unknown.com')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], "Domain 'unknown.com' not found")

    def test_resolve_no_domain(self):
        # Test when no domain is provided
        response = self.client.get('/resolve')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], "No domain provided")

    def test_resolve_with_whitespace(self):
        # Test domain input with leading/trailing whitespace
        response = self.client.get('/resolve?domain= example.com ')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['ip'], '192.168.1.10')

if __name__ == '__main__':
    unittest.main()
