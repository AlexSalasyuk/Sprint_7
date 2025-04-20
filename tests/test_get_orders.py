import requests
import allure
from urls import BASE_URL

GET_ORDERS_URL = f'{BASE_URL}/api/v1/orders'


@allure.title('Проверить получение списка заказов')
class TestGetOrders:
    @allure.step('Проверить, что ручка возвращает список заказов')
    def test_get_orders_return_list(self):
        response = requests.get(GET_ORDERS_URL)

        with allure.step('Проверить статус код 200, в теле ответа список заказов'):
            assert response.status_code == 200
            assert 'orders' in response.json()
            assert isinstance(response.json()['orders'], list)
