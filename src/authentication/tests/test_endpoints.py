import pytest
from rest_framework import status
from authentication import models


@pytest.mark.parametrize(
    "url, num_records, exp_status",
    [
        pytest.param("/authentication/user/", 2, status.HTTP_200_OK),
        pytest.param("/authentication/attendant/", 1, status.HTTP_200_OK),
    ],
)
@pytest.mark.django_db
def test_get_data_users(client_admin, load_all_fixtures_for_function, url, num_records, exp_status):
    response = client_admin.get(path=url)
    assert response.data.__len__() == num_records
    assert response.status_code == exp_status


@pytest.mark.parametrize(
    "url, role, exp_status",
    [
        pytest.param("/authentication/user/1/", models.UserRoleChoice.ADMIN.name, status.HTTP_200_OK),
        pytest.param("/authentication/user/2/", models.UserRoleChoice.ATTENDANT.name, status.HTTP_200_OK),
    ],
)
@pytest.mark.django_db
def test_get_data_users_by_id(client_admin, load_all_fixtures_for_module, url, role, exp_status):
    response = client_admin.get(path=url)
    assert response.data["role"] == role
    assert response.status_code == exp_status


@pytest.mark.parametrize(
    "url, payload, exp_status",
    [
        pytest.param(
            "/authentication/attendant/",
            {"email": "a@a.com", "password": "aaaaaaaa", "old_or_verify_password": "aaaaaaaa"},
            status.HTTP_201_CREATED,
        ),
        pytest.param(
            "/authentication/attendant/",
            {"email": "c@c.com", "password": "aaaaaaaa", "old_or_verify_password": "cccccccc"},
            status.HTTP_400_BAD_REQUEST,
        ),
    ],
)
@pytest.mark.django_db
def test_create_user(client_admin, url, payload, exp_status):
    response = client_admin.post(path=url, data=payload, format="json")
    assert response.status_code == exp_status

    if exp_status == status.HTTP_201_CREATED:
        assert payload["email"] == response.data["email"]
        assert "ATTENDANT" == response.data["role"]


@pytest.mark.django_db
def test_update_admin_by_admin(client_admin, load_all_fixtures_for_function):
    payload = {"password": "bbbbbbbb", "old_or_verify_password": "a"}
    response_update = client_admin.patch(path="/authentication/user/1/", data=payload, format="json")

    payload_auth = {"email": response_update.data["email"], "password": "bbbbbbbb"}
    response_auth = client_admin.post("/authentication/token/create/", data=payload_auth)

    assert response_update.status_code == status.HTTP_200_OK
    assert response_auth.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_attendant_by_admin(client_admin, client, test_login_required, load_all_fixtures_for_function):
    payload = {"password": "bbbbbbbb", "old_or_verify_password": "a"}
    response_update = client_admin.patch(path="/authentication/attendant/2/", data=payload, format="json")

    payload_auth = {"email": response_update.data["email"], "password": "bbbbbbbb"}
    response_auth = client.post("/authentication/token/create/", data=payload_auth)

    assert response_update.status_code == status.HTTP_200_OK
    assert response_auth.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_attendant_by_myself(client_attendant, client, attendant, test_login_required):
    payload = {"password": "bbbbbbbb", "old_or_verify_password": attendant[1]["password"]}
    response_update = client_attendant.patch(
        path=f"/authentication/attendant/{attendant[0].id}/", data=payload, format="json"
    )

    payload_auth = {"email": response_update.data["email"], "password": "bbbbbbbb"}
    response_auth = client.post("/authentication/token/create/", data=payload_auth)

    assert response_update.status_code == status.HTTP_200_OK
    assert response_auth.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.skip
def test_password_validator():
    pass


@pytest.mark.django_db
@pytest.mark.skip
def test_password_and_old_or_verify_password_create():
    pass


@pytest.mark.django_db
@pytest.mark.skip
def test_password_and_old_or_verify_password_update():
    pass
