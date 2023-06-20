from django.test import Client, TestCase
from django.urls import reverse

ru_headers = {"Accept-Language": "ru"}
en_headers = {"Accept-Language": "en"}
b = '<input class="btn btn-primary" type="submit" value="Зарегистрировать">'


class MainTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.main_url = reverse("main")

    def test_main_page_status(self):
        response = self.client.get(self.main_url)
        self.assertEquals(response.status_code, 200)

    def test_ru_content(self):
        response = self.client.get(self.main_url, headers=ru_headers)
        # self.client.
        self.assertIn(
            "Менеджер задач", str(response._container[0].decode("utf-8"))
        )
        self.assertIn(
            "Инструмент для идеального управления вашими задачами",
            str(response._container[0].decode("utf-8")),
        )
        self.assertEquals(response.headers.get("Content-Language"), "ru")

    def test_en_content(self):
        response = self.client.get(self.main_url, headers=en_headers)
        self.assertIn("Task Manager", response._container[0].decode("utf-8"))
        self.assertIn(
            "Tool for perfect managing your tasks",
            response._container[0].decode("utf-8"),
        )
        self.assertEquals(response.headers.get("Content-Language"), "en-us")


class Login(TestCase):
    def setUp(self):
        self.client = Client()
        self.main_url = reverse("login")

    def test_main_page_status(self):
        response = self.client.get(self.main_url)
        self.assertEquals(response.status_code, 200)

    def test_ru_content(self):
        response = self.client.get(self.main_url, headers=ru_headers)
        self.assertIn(
            '<h1 class="my-4">Вход</h1>',
            str(response._container[0].decode("utf-8")),
        )
        self.assertIn(
            '<label for="id_for_username">Имя пользователя</label>',
            str(response._container[0].decode("utf-8")),
        )
        self.assertIn(
            '<label for="id_for_password">Пароль</label>',
            str(response._container[0].decode("utf-8")),
        )
        self.assertIn(
            '<input class="btn btn-primary" type="submit" value="Войти">',
            str(response._container[0].decode("utf-8")),
        )
        self.assertEquals(response.headers.get("Content-Language"), "ru")

    def test_en_content(self):
        response = self.client.get(self.main_url, headers=en_headers)
        self.assertIn(
            '<h1 class="my-4">Login</h1>',
            str(response._container[0].decode("utf-8")),
        )
        self.assertIn(
            '<label for="id_for_username">Username</label>',
            str(response._container[0].decode("utf-8")),
        )
        self.assertIn(
            '<label for="id_for_password">Password</label>',
            str(response._container[0].decode("utf-8")),
        )
        self.assertIn(
            '<input class="btn btn-primary" type="submit" value="Login">',
            str(response._container[0].decode("utf-8")),
        )
        self.assertEquals(response.headers.get("Content-Language"), "en-us")
