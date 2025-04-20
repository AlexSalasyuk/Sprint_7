import pytest
import requests
from helpers import register_new_courier_and_return_login_password
from urls import BASE_URL

DELETE_COURIER_URL = f'{BASE_URL}/api/v1/courier'

@pytest.fixture
def courier():
    creds = register_new_courier_and_return_login_password()
    assert creds, "Не удалось создать курьера"
    login, password, _ = creds

    login_resp = requests.post(f"{BASE_URL}/api/v1/courier/login", json={
        "login": login,
        "password": password
    })
    courier_id = login_resp.json().get("id")

    yield creds

    if courier_id:
        requests.delete(f"{DELETE_COURIER_URL}/{courier_id}")
