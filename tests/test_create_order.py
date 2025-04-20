import requests
import allure
import pytest
from urls import BASE_URL

CREATE_ORDER_URL = f'{BASE_URL}/api/v1/orders'

@allure.title('Проверить создание заказа')
class TestCreateOrder:
    @allure.step('Проверить создание заказа с разными вариантами цвета')
    @pytest.mark.parametrize('color', [
        ['BLACK'],
        ['GREY'],
        ['BLACK', 'GREY'],
        []
    ])
    def test_create_order_different_colors_return_track(self, color):
        payload = {
            'firstName': 'Sunny',
            'lastName': 'Sun',
            'address': 'Sri-Lanka, 42 apt.',
            'metroStation': 4,
            'phone': '88005553535',
            'rentTime': 42,
            'deliveryDate': '2025-05-04',
            'comment': 'Bring Me Track Fixed Gear Bike',
            'color': color
        }

        response = requests.post(CREATE_ORDER_URL, json=payload)

        with allure.step('Проверить, что статус код 201  и есть поле track'):
            assert response.status_code == 201
            assert 'track' in response.json()
