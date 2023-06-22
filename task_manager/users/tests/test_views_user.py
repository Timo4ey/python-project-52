from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse_lazy

from task_manager.tests.conftest import TestUserSetUp

ru_headers = {"Accept-Language": "ru"}
en_headers = {"Accept-Language": "en"}
b = '<input class="btn btn-primary" type="submit" value="Зарегистрировать">'


class TestRegistration(TestCase):
    def setUp(self):
        self.client = Client()
        self.main_url = reverse_lazy("create_user")

    def test_main_page_status(self):
        response = self.client.get(self.main_url)
        self.assertEquals(response.status_code, 200)

    def test_ruPlease_content(self):
        response = self.client.get(self.main_url, headers=ru_headers)
        self.assertIn(
            '<h1 class="my-4">Регистрация</h1>',
            str(response._container[0].decode("utf-8")),
        )

        self.assertIn(
            '<label for="id_first_name">Имя</label>',
            str(response._container[0].decode("utf-8")),
        )

        self.assertIn(
            '<label for="id_last_name">Фамилия</label>',
            str(response._container[0].decode("utf-8")),
        )

        self.assertIn(
            '<label for="id_password1">Пароль</label>',
            str(response._container[0].decode("utf-8")),
        )
        self.assertIn(
            '<label for="id_password2">Подтверждение пароля</label>',
            str(response._container[0].decode("utf-8")),
        )

        self.assertIn(b, str(response._container[0].decode("utf-8")))

        self.assertEquals(response.headers.get("Content-Language"), "ru")

    def test_en_content(self):
        response = self.client.get(self.main_url, headers=en_headers)
        self.assertIn(
            '<h1 class="my-4">Registration</h1>',
            str(response._container[0].decode("utf-8")),
        )

        self.assertIn(
            '<label for="id_username">Username</label>',
            str(response._container[0].decode("utf-8")),
        )

        self.assertIn(
            '<label for="id_last_name">Last name</label>',
            str(response._container[0].decode("utf-8")),
        )

        self.assertIn(
            '<label for="id_password1">Password</label>',
            str(response._container[0].decode("utf-8")),
        )

        self.assertIn(
            '<label for="id_password2">Password confirmation</label>',
            str(response._container[0].decode("utf-8")),
        )

        self.assertIn(
            '<input class="btn btn-primary" type="submit" value="Registrate">',
            str(response._container[0].decode("utf-8")),
        )

        self.assertEquals(response.headers.get("Content-Language"), "en-us")


class TestUsersViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.main_url = reverse_lazy("users")

    def test_main_page_status(self):
        response = self.client.get(self.main_url)
        self.assertEquals(response.status_code, 200)

    def test_ruPlease_content(self):
        response = self.client.get(self.main_url, headers=ru_headers)
        self.assertIn(
            '<h1 class="my-4">Пользователи</h1>',
            str(response._container[0].decode("utf-8")),
        )

        self.assertIn(
            "<th>ID</th>", str(response._container[0].decode("utf-8"))
        )

        self.assertIn(
            "<th>Имя пользователя</th>",
            str(response._container[0].decode("utf-8")),
        )

        self.assertIn(
            "<th>Полное имя</th>", str(response._container[0].decode("utf-8"))
        )
        self.assertIn(
            "<th>Дата создания</th>",
            str(response._container[0].decode("utf-8")),
        )

        self.assertEquals(response.headers.get("Content-Language"), "ru")

    def test_en_content(self):
        response = self.client.get(self.main_url, headers=en_headers)
        self.assertIn(
            '<h1 class="my-4">Users</h1>',
            str(response._container[0].decode("utf-8")),
        )

        self.assertIn(
            "<th>ID</th>", str(response._container[0].decode("utf-8"))
        )

        self.assertIn(
            "<th>Username</th>", str(response._container[0].decode("utf-8"))
        )

        self.assertIn(
            "<th>Full name</th>", str(response._container[0].decode("utf-8"))
        )
        self.assertIn(
            "<th>Created at</th>", str(response._container[0].decode("utf-8"))
        )

        self.assertEquals(response.headers.get("Content-Language"), "en-us")


class TestUsersUpdate(TestUserSetUp):
    def test_views_update_user_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})

        response = self.client.get(
            reverse_lazy("update_user", kwargs={"id": self.user.id})
        )
        self.assertIn(
            '<h1 class="my-4">Update user</h1>',
            response.content.decode("utf-8"),
        )

        self.assertIn(
            '<label for="id_username">Username</label>',
            str(response.content.decode("utf-8")),
        )

        self.assertIn(
            '<label for="id_last_name">Last name</label>',
            str(response.content.decode("utf-8")),
        )

        self.assertIn(
            '<label for="id_password1">Password</label>',
            str(response.content.decode("utf-8")),
        )

        self.assertIn(
            '<label for="id_password2">Password confirmation</label>',
            str(response.content.decode("utf-8")),
        )

        self.assertIn(
            '<input class="btn btn-primary" type="submit" value="Update">',
            str(response.content.decode("utf-8")),
        )

    def test_views_update_user_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        response = self.client.get(
            reverse_lazy("update_user", kwargs={"id": self.user.id})
        )
        self.assertIn(
            '<h1 class="my-4">Изменение пользователя</h1>',
            response.content.decode("utf-8"),
        )

        self.assertIn(
            '<label for="id_first_name">Имя</label>',
            str(response.content.decode("utf-8")),
        )

        self.assertIn(
            '<label for="id_last_name">Фамилия</label>',
            str(response.content.decode("utf-8")),
        )

        self.assertIn(
            '<label for="id_password1">Пароль</label>',
            str(response.content.decode("utf-8")),
        )

        self.assertIn(
            '<label for="id_password2">Подтверждение пароля</label>',
            str(response.content.decode("utf-8")),
        )

        self.assertIn(
            '<input class="btn btn-primary" type="submit" value="Изменить">',
            str(response.content.decode("utf-8")),
        )
