import pytest
import requests
import allure
from urls import BASE_URL

LOGIN_URL = f'{BASE_URL}/api/v1/courier/login'


@allure.title('Проверить авторизацию курьера')
class TestLoginCourier:

    @allure.step('Проверить, что курьер может авторизоваться')
    def test_login_valid_data_return_id(self, courier):
        login, password, _ = courier

        login_payload = {
            'login': login,
            'password': password
        }

        response = requests.post(LOGIN_URL, json=login_payload)

        with allure.step('Проверить, что пришёл статус код 200 и в ответе есть id'):
            assert response.status_code == 200
            assert 'id' in response.json()

    @allure.step('Проверить ошибку при авторизации без обязательных полей')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_login_missing_required_field_error_400(self, missing_field, courier):
        login, password, _ = courier

        login_payload = {
            'login': login,
            'password': password
        }

        del login_payload[missing_field]

        if missing_field == 'password':
            pytest.xfail('БАГ: 504 Gateway Timeout. Сервер зависает при отсутствии поля password')

        response = requests.post(LOGIN_URL, json=login_payload)

        with allure.step('Проверить, что при отсутствии поля "{missing_field}" статус код 400 и сообщение о нехватке данных'):
            assert response.status_code == 400
            assert response.json()['message'] == 'Недостаточно данных для входа'

    @allure.step('Проверить ошибку при авторизации с неправильным логином или паролем')
    @pytest.mark.parametrize('wrong_field', ['login', 'password'])
    def test_login_wrong_login_or_password_error_404(self, wrong_field, courier):
        login, password, _ = courier

        login_payload = {
            'login': login,
            'password': password
        }

        login_payload[wrong_field] = login_payload[wrong_field] + '_wrong'

        response = requests.post(LOGIN_URL, json=login_payload)

        with allure.step('Проверить, что при неправильном "{wrong_field}" статус код 404 и сообщение о несуществующей учётной записи'):
            assert response.status_code == 404
            assert response.json()['message'] == 'Учетная запись не найдена'

    @allure.step('Проверить авторизацию несуществующего пользователя')
    def test_login_not_exist_user_error_404(self):
        payload = {
            'login': 'not_exist_user_error',
            'password': 'push_the_button'
        }

        response = requests.post(LOGIN_URL, json=payload)

        with allure.step('Проверить, статус код 404 и сообщение о несуществующей учётной записи'):
            assert response.status_code == 404
            assert response.json()['message'] == 'Учетная запись не найдена'
