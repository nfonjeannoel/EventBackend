import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestAttendance(unittest.TestCase):
    email = "test4@gmail.com"
    password = "password123"
    full_name = "Test User"
    event_data = {
        "name": "Test Event",
        "date": "2023-06-12",
        "details": "Test event details",
        "start_time": "09:00",
        "end_time": "12:00"
    }

    headers = {}

    def setUp(self):
        self.create_user()
        self.access_token = self.login_and_get_token()
        self.headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

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

    def create_event(self):
        response = client.post("/api/create_event", json=self.event_data, headers=self.headers)
        return response.json()

    def test_create_attendance(self):
        event = self.create_event()
        rsvp_data = {
            "event_id": event["id"],
        }
        response = client.post("/api/create_rsvp", json=rsvp_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["event_id"], event["id"])

    def test_get_my_rsvps(self):
        self.create_event()
        response = client.get("/api/my_rsvps", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        # Add assertions to validate the response data
