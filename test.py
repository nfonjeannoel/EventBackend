import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

from Users.test_users import TestUserModel as _TestUserModel
from Events.test_events import TestEventModel as _TestEventModel
from Venues.test_venues import TestVenueModel as _TestVenueModel
from Attendances.test_attendance import TestAttendance as _TestAttendance


class TestUserModel(_TestUserModel):
    pass


class TestEventModel(_TestEventModel):
    pass


class TestVenueModel(_TestVenueModel):
    pass


class TestAttendance(_TestAttendance):
    pass


if __name__ == '__main__':
    unittest.main()
