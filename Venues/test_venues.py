import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestVenueModel(unittest.TestCase):
    email = "test2@gmail.com"
    password = "password123"
    full_name = "Test User"

    def setUp(self):
        self.access_token = self.login_and_get_token()

    def login_and_get_token(self):
        login_data = {
            "username": self.email,
            "password": self.password
        }
        response = client.post("/api/token", data=login_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["token_type"], "bearer")
        return response.json()["access_token"]

    def test_create_venue(self):
        venue_data = {
            "location": "Test Location",
            "description": "Test venue description",
            "pictures": "Test pictures",
            "name": "Test Venue",
            "price_per_hour": 100.0,
            "dimension": "Test dimension",
            "capacity": 100
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = client.post("/api/create_venue", json=venue_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Venue")

    def test_get_venue_by_id(self):
        venue_id = self.create_venue_and_get_id()
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        print(headers)
        response = client.get(f"/api/venue/{venue_id}", headers=headers)
        self.assertEqual(response.status_code, 200)
        # Add assertions to validate the response data

    def create_venue_and_get_id(self):
        venue_data = {
            "location": "Test Location",
            "description": "Test venue description",
            "pictures": "Test pictures",
            "name": "Test Venue",
            "price_per_hour": 100.0,
            "dimension": "Test dimension",
            "capacity": 100
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = client.post("/api/create_venue", json=venue_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        return response.json()["id"]
