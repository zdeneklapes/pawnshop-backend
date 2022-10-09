import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
def test_after_maturity_response_data_for_product(login_client, load_all_fixtures_for_module):
    pass


@pytest.mark.django_db
@pytest.mark.xfail
def test_after_maturity_to_offer_quantity():
    pass
