from rest_framework.test import APITestCase


class TestLoan(APITestCase):
    def test_create_unauthenticated_loan(self):
        self.assert_(False, "Not Implemented")

    def test_create_authenticated_loan(self):
        self.assert_(False, "Not Implemented")

    def test_cancel_load_return_product(self):
        self.assert_(False, "Not Implemented")

    def test_loan_one_day_after_date_end(self):
        self.assert_(False, "Not Implemented")

    def test_loan_more_than_one_day_after_date_end(self):
        self.assert_(False, "Not Implemented")

    def test_loan_extend_date(self):
        self.assert_(False, "Not Implemented")

    def test_loan_sell_price_for_each_week(self):
        self.assert_(False, "Not Implemented")
