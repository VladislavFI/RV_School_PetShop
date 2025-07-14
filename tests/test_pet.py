import allure
import requests
import jsonschema
import pytest
from .schemas.pet_schema import PET_SCHEMA

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

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()["id"] == pet_id

    @allure.title("Обновление информации о питомце")
    def test_update_pet_info(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        payload = {
            "id": pet_id,
            "name": "Buddy Updated",
            "status": "sold"
        }

        with allure.step("Отправка запроса на обновление информации о питомце по ID"):
            response = requests.put(f"{BASE_URL}/pet/", json=payload)
            response_json = response.json()

            assert response.status_code == 200
            assert response_json["id"] == payload["id"], "Id питомца не совпал с ожидаемым"
            assert response_json["name"] == payload["name"], "Имя питомца не совпало с ожидаемым"
            assert response_json["status"] == payload["status"], "Статус питомца не совпал с ожидаемым"

    @allure.title("Удаление питомца по ID ")
    def test_delete_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на удаление питомца по ID"):
            response = requests.delete(f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 200

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 404

    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [
            ("available", 200),
            ("pending", 200),
            ("sold", 200),
            ("abcd", 400),
            ("", 400),
        ]
    )
    def test_get_pets_by_status(self, status, expected_status_code):
        with allure.step(f"Отправка запроса на получение питомцев по статусу {status}"):
            response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": status})

        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == expected_status_code
            if response.status_code == 200:
                assert isinstance(response.json(), list)
            else:
                assert response.status_code == expected_status_code
