import pytest


def pytest_configure():
    product_urls = {}
    pytest.product_urls = product_urls
