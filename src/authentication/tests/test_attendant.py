from rest_framework.test import APITestCase


class TestAttendant(APITestCase):
    def test_attendant_can_create_only_customer_profile(self):
        self.assert_(False, "Not Implemented")
