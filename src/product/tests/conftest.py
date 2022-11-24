import pytest

from statistic.models.choices import StatisticDescription


class TestProductData:
    data_update = {
        "update": f"{StatisticDescription.UPDATE_DATA.name}",
        "product_name": "Telefon Samsung 111",
        "date_create": "2022-09-05T14:31:47.080000Z",
        "date_extend": "2022-09-05T14:31:47.080000Z",
        "status": "OFFERrrr",
        "customer": {
            "full_name": "a b",
            "residence": "Cejl 222",
            "sex": "F",
            "nationality": "SK",
            "personal_id": "0000000000",
            "personal_id_expiration_date": "2023-02-02",
            "birthplace": "Prha",
            "id_birth": "000000/0001",
        },
        "interest_rate_or_quantity": "1.0",
        "inventory_id": 111,
        "buy_price": 100,
        "sell_price": 11111,
    }


def pytest_configure():
    product_urls = {}
    pytest.product_urls = product_urls
    pytest.UpdateProductData = TestProductData
