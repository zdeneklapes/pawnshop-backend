from rest_framework.test import APITestCase

# from . import models  # TODO: Why does this not working?
# from shop.models import Shop  # TODO: Must be like this


class TestGroupAllPermision:
    pass


class TestAttendantCreate(APITestCase):
    def test_user_is_authenticated_ok(self):
        self.assert_(False, "Not Implemented")

    def test_user_is_authenticated_error(self):
        self.assert_(False, "Not Implemented")

    def test_user_is_allowed_to_create_attendant_ok(self):
        self.assert_(False, "Not Implemented")

    def test_user_is_allowed_to_create_attendant_error(self):
        self.assert_(False, "Not Implemented")

    def test_user_creation_ok(self):
        self.assert_(False, "Not Implemented")

    def test_user_creation_error(self):
        self.assert_(False, "Not Implemented")
