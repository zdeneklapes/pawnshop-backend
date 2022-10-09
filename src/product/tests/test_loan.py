import pytest
from rest_framework import status
from product.models import ProductStatusOrData


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path_url, exp_status",
    [
        pytest.param(f"/product/?data={ProductStatusOrData.LOAN.name}", status.HTTP_200_OK),
    ],
)
def test_loan_interest_and_sell_price_response(login_client, load_all_fixtures, path_url, exp_status):
    response = login_client.get(path=path_url)
    assert response.status_code == exp_status

    # for i in response.data:
    #     pass


@pytest.mark.django_db
@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
def test_loan_response_data_for_product(login_client, load_all_fixtures):
    pass


@pytest.mark.django_db
@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
def test_loan_create_calculations(login_client, load_all_fixtures):
    pass


@pytest.mark.django_db
@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
def test_loan_extend_calculations(login_client, load_all_fixtures):
    pass
