import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestEventModel(unittest.TestCase):
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

    def test_create_event(self):
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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Event")

    def test_update_event(self):
        event_id = self.create_event_and_get_id()
        event_data = {
            "name": "Updated Event",
            "date": "2023-06-15",
            "details": "Updated event details",
            "start_time": "10:00",
            "end_time": "13:00"
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = client.put(f"/api/event/{event_id}", json=event_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Updated Event")

    def test_get_all_events(self):
        response = client.get("/api/all_events")
        self.assertEqual(response.status_code, 200)
        # Add assertions to validate the response data

    def test_get_events_by_owner(self):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = client.get("/api/events/me", headers=headers)
        self.assertEqual(response.status_code, 200)
        # Add assertions to validate the response data

    def create_event_and_get_id(self):
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
        self.assertEqual(response.status_code, 200)
        return response.json()["id"]
