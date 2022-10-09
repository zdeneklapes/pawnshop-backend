import pytest


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_loan_create(login_client):
    assert False


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_loan_extend(login_client):
    assert False


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_loan_return(login_client):
    assert False


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_after_maturity_return(login_client):
    assert False


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_after_aturity_extend(login_client):
    assert False


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_offer_create(login_client):
    assert False


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_offer_buy(login_client):
    assert False


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_offer_sell(login_client):
    assert False


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_statistic_default_data(login_client):
    assert False


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_statistic_daily_stats_data(login_client):
    assert False


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_statistic_cash_amount_data(login_client):
    assert False


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_statistic_reset_profit(login_client):
    assert False
