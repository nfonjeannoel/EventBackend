import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestUserModel(unittest.TestCase):
    email = "test2@gmail.com"
    password = "password123"
    full_name = "Test User"

    def test_create_user(self):
        user_data = {
            "email": self.email,
            "password": self.password,
            "full_name": self.full_name
        }
        response = client.post("/api/create_user", json=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["token_type"], "bearer")

    def test_login(self):
        login_data = {
            "username": self.email,
            "password": self.password
        }
        response = client.post("/api/token", data=login_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["token_type"], "bearer")
        self.access_token = response.json()["access_token"]

    def test_read_users(self):
        response = client.get("/api/users")
        self.assertEqual(response.status_code, 200)
        # Add assertions to validate the response data

    def test_read_users_me_unauthorized(self):
        response = client.get("/api/users/me")
        self.assertEqual(response.status_code, 401)  # Unauthorized without authentication

    def test_read_users_me_authorized(self):
        # make request and get token
        response = client.post("/api/token", data={"username": self.email, "password": self.password})
        token = response.json()["access_token"]
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = client.get("/api/users/me", headers=headers)
        self.assertEqual(response.status_code, 200)
        # Add assertions to validate the response data
