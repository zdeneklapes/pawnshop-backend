import pytest
from rest_framework import status
from deepdiff import DeepDiff


@pytest.mark.django_db
@pytest.mark.parametrize(
    "product_id, payload_data, exp_status_patch, exp_status_get",
    [
        pytest.param(1, pytest.UpdateProductData.data_update, status.HTTP_200_OK, status.HTTP_200_OK),
    ],
)
def test_update_loan(load_all_scope_function, client_admin, product_id, payload_data, exp_status_patch, exp_status_get):
    response_get_prev = client_admin.get(path=f"/product/{product_id}/")
    client_admin.patch(path=f"/product/{product_id}/", data=payload_data, format="json")
    response_get = client_admin.get(path=f"/product/{product_id}/")

    diff_paths = ["product_name", "inventory_id", "date_create", "date_extend"]
    diff = DeepDiff(response_get_prev.data, response_get.data, ignore_order=True, exclude_paths=["interest"])
    diff_error = DeepDiff(diff_paths, diff.affected_root_keys.items, ignore_order=True)

    if diff_error.__len__() != 0:
        print(diff_error)

    assert diff_error.__len__() == 0
