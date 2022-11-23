from deepdiff import DeepDiff

import pytest
from rest_framework import status
from statistic.models import StatisticDescription


@pytest.mark.django_db
@pytest.mark.parametrize(
    "product_id, payload_data, exp_status_patch, exp_status_get",
    [
        pytest.param(
            4,
            {
                "update": f"{StatisticDescription.UPDATE_DATA.name}",
                "product_name": "Telefon Samsung 1",
                "date_create": "2022-09-01T14:31:47.080000Z",
                "date_extend": "2022-09-01T14:31:47.080000Z",
                "status": "OFFER",
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
                "inventory_id": 3,
                "buy_price": 100,
                "sell_price": 200,
            },
            status.HTTP_200_OK,
            status.HTTP_200_OK,
        ),
    ],
)
def test_update_offer(
    load_all_fixtures_for_function, client_attendant, product_id, payload_data, exp_status_patch, exp_status_get
):
    response_get_prev = client_attendant.get(path=f"/product/{product_id}/")
    client_attendant.patch(path=f"/product/{product_id}/", data=payload_data, format="json")
    response_get = client_attendant.get(path=f"/product/{product_id}/")

    diff_paths = ["product_name", "inventory_id"]
    diff = DeepDiff(response_get_prev.data, response_get.data, ignore_order=True)
    diff_error = DeepDiff(diff_paths, diff.affected_root_keys.items, ignore_order=True)

    assert diff_error.__len__() == 0
