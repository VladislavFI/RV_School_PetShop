import allure
import requests
import jsonschema
from .schemas.pet_schema import  PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
             response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текста ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение несуществующего питомца"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текста ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response.json(), PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "Id питомца не совпал с ожидаемым"
            assert response_json['name'] == payload['name'], "Имя питомца не совпало с ожидаемым"
            assert response_json['status'] == payload['status'], "Статус питомца не совпал с ожидаемым"

    @allure.title("Добавление нового питомца c полными данными")
    def test_add_pet_full_data(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {"id": 1, "name": "Dogs"},
                "photoUrls": ["string"],
                "tags": [{"id": 0, "name": "string"}],
                "status": "available"
            }

            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка cтруктуры ответа"):
            jsonschema.validate(response.json(), PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "Id питомца не совпал с ожидаемым"
            assert response_json['name'] == payload['name'], "Имя питомца не совпало с ожидаемым"
            assert response_json['category'] == payload['category'], "Категория питомца не совпала с ожидаемым"
            assert response_json['photoUrls'] == payload['photoUrls'], "Url фотографии питомца не совпала с ожидаемым"
            assert response_json['tags'] == payload['tags'], "Тэг питомца не совпал с ожидаемым"
            assert response_json['status'] == payload['status'], "Статус питомца не совпал с ожидаемым"

