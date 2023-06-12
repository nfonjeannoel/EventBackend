import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestVenueModel(unittest.TestCase):
    email = "test3@gmail.com"
    password = "password123"
    full_name = "Test User"

    venue_data = {
        "location": "Test Location",
        "description": "Test venue description",
        "pictures": "Test pictures",
        "name": "Test Venue",
        "price_per_hour": 100.0,
        "dimension": "Test dimension",
        "capacity": 100
    }

    def setUp(self):
        self.create_user()
        self.access_token = self.login_and_get_token()

    def create_Event(self):
        event_data = {
            "name": "Test Event",
            "date": "2023-06-12",
            "details": "Test event details",
            "start_time": "09:00",
            "end_time": "12:00"
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = client.post("/api/create_event", json=event_data, headers=headers)
        return response.json()

    def create_user(self):
        user_data = {
            "email": self.email,
            "password": self.password,
            "full_name": self.full_name
        }
        response = client.post("/api/create_user", json=user_data)
        if response.status_code != 200:
            # User already exists
            pass
        else:
            self.assertEqual(response.status_code, 200)

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
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = client.post("/api/create_venue", json=self.venue_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Venue")

    def test_create_event_venue(self):
        event = self.create_Event()
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = client.post(f"/api/create_event_venue/{event['id']}", json=self.venue_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Venue")

    # def test_get_venue_by_id(self):
    #     venue_id = self.create_venue_and_get_id()
    #     headers = {
    #         "Authorization": f"Bearer {self.access_token}"
    #     }
    #     response = client.get(f"/api/venue/{venue_id}", headers=headers)
    #     self.assertEqual(response.status_code, 200)
    #     # Add assertions to validate the response data
