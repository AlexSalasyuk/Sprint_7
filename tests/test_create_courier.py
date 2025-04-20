import pytest
import requests
import allure
import random
import string
from urls import BASE_URL

CREATE_COURIER_URL = f'{BASE_URL}/api/v1/courier'

def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

@allure.title('Проверить создание курьера')
class TestCreateCourier:
    @allure.step('Проверить, что курьера можно создать')
    def test_create_courier_all_fields_201_ok_true(self):
        payload = {
            'login': generate_random_string(10),
            'password': generate_random_string(10),
            'firstName': generate_random_string(10)
        }

        response = requests.post(CREATE_COURIER_URL, data=payload)

        with allure.step('Проверить статус код 201 и тело ответа'):
            assert response.status_code == 201
            assert response.json() == {'ok': True}

    @allure.step('Проверить, что нельзя создать двух одинаковых курьеров')
    def test_create_courier_same_login_error_409(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            'login': login,
            'password': password,
            'firstName': first_name
        }

        response_1 = requests.post(CREATE_COURIER_URL, data=payload)

        assert response_1.status_code == 201
        assert response_1.json() == {'ok': True}

        response_2 = requests.post(CREATE_COURIER_URL, data=payload)

        with allure.step('Проверить, что повторный запрос отклонён, статус код 409'):
            assert response_2.status_code == 409
            assert response_2.json()['message'] == 'Этот логин уже используется. Попробуйте другой.'


    @allure.step('Проверить создание курьера без одного из обязательных полей')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_create_courier_missing_required_field_error_400(self, missing_field):
        payload = {
            'login': generate_random_string(10),
            'password': generate_random_string(10),
            'firstName': generate_random_string(10)
        }

        del payload[missing_field]

        response = requests.post(CREATE_COURIER_URL, data=payload)

        with allure.step('Проверить, что при отсутствии поля "{missing_field}" приходит статус код 400 и сообщение о нехватке данных'):
            assert response.status_code == 400
            assert response.json()['message'] == 'Недостаточно данных для создания учетной записи'


    @allure.step('Проверить создание курьера с уже существующим логином')
    def test_create_courier_exist_login_error_409(self, courier):
        login, _, _ = courier

        payload = {
            'login': login,
            'password': generate_random_string(10),
            'firstName': generate_random_string(10)
        }

        response = requests.post(CREATE_COURIER_URL, data=payload)

        with allure.step('Проверить, что повторный логин вернёт статус код 409 и сообщение о использовании логина'):
            assert response.status_code == 409
            assert response.json()['message'] == 'Этот логин уже используется. Попробуйте другой.'

