import pytest

from product.models import ProductShopData, ProductStatusOrData


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path_data",
    [
        pytest.param(f"/product/?data={ProductShopData.SHOP_STATS.name}"),
    ],
)
def test_shop_stat_expected_data(client_admin, load_all_scope_module, path_data):
    response = client_admin.get(path=path_data)

    assert response.data.__len__() == 3
    assert {"status", "count", "sell", "buy"} <= set(response.data[0])
    for item in response.data:
        assert item["status"] in [
            ProductStatusOrData.LOAN.label,
            ProductStatusOrData.OFFER.label,
            ProductStatusOrData.AFTER_MATURITY.label,
        ]
