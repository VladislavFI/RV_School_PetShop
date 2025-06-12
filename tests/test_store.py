import allure
import requests
import jsonschema
import pytest
from .schemas.store_schema import INVENTORY_SCHEMA


BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_create_order(self):
        payload = {
            "id": 1, "petId": 1,
            "quantity": 1,
            "status": "placed",
            "complete": True
        }

        with allure.step("Отправка запроса на размещение заказа"):
             response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
             response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка параметров заказа в ответе"):
            assert response_json['id'] == payload['id'], "id заказа не совпал с ожидаемым"
            assert response_json['quantity'] == payload['quantity'], "Кол-во заказа не совпало с ожидаемым"
            assert response_json['status'] == payload['status'], "Статус питомца не совпал с ожидаемым"
            assert response_json['complete'] == payload['complete'], "Параметр complete заказа не совпал с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_info(self):

        expected_result = {
            "id": 1,
            "petId": 1,
            "quantity": 1,
            "status": "placed",
            "complete": True
        }

        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка данных заказа в ответе "):
            assert response_json['id'] == expected_result['id'], "Id заказа не совпал с ожидаемым"
            assert response_json['quantity'] == expected_result['quantity'], "Кол-во заказа не совпал с ожидаемым"
            assert response_json['status'] == expected_result['status'], "Статус заказа не совпало с ожидаемым"
            assert response_json['complete'] == expected_result['complete'], "Параметр complete не совпал с ожидаемым"

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self, create_store):
        store_id = create_store["id"]

        with allure.step("Отправка запроса на удаление питомца"):
            response = requests.delete(url=f"{BASE_URL}/store/order/{store_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на удаление питомца"):
            response = requests.get(url=f"{BASE_URL}/store/order/{store_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_store(self):
        with allure.step("Отправка запроса на получение несуществующего заказа"):
            response = requests.get(url=f"{BASE_URL}/store/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory_store(self, create_store):

        with allure.step("Отправка запроса на получение инвентаря магазина"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка cтруктуры ответа"):
            jsonschema.validate(response.json(), INVENTORY_SCHEMA)



