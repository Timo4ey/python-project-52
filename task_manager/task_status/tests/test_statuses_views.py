from django.conf import settings
from django.test import modify_settings
from django.urls import reverse_lazy

from task_manager.task_status.models import TaskStatus
from task_manager.tests.conftest import TestStatusSetUp, data


@modify_settings(
    MIDDLEWARE={
        "remove": [
            "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
        ]
    }
)
class TestStatusIndexPage(TestStatusSetUp):
    def test_empty_main_page(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        status = TaskStatus.objects.get(name=data["status"]["name"])
        status.delete()

        response = self.client.get(reverse_lazy("statuses"))
        content = response.content.decode("utf-8")
        self.assertNotIn('<a href="/statuses/1/update/">Изменить</a>', content)
        self.assertNotIn('<a href="/statuses/1/delete/">Удалить</a>', content)

    def test_main_page_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        response = self.client.get(reverse_lazy("statuses"))
        content = response.content.decode("utf-8")
        # h1
        self.assertIn('<h1 class="my-4">Statuses</h1>', content)
        # Table
        self.assertIn("<th>ID</th>", content)
        self.assertIn("<th>Name</th>", content)
        self.assertIn("<th>Created at</th>", content)
        self.assertIn(data["status"]["name"], content)

        # Update link
        self.assertIn('<a href="/statuses/1/update/">Update</a>', content)
        self.assertIn('<a href="/statuses/1/delete/">Delete</a>', content)

    def test_main_page_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})
        response = self.client.get(reverse_lazy("statuses"))
        content = response.content.decode("utf-8")
        # h1
        self.assertIn('<h1 class="my-4">Статусы</h1>', content)
        # Table
        self.assertIn("<th>ID</th>", content)
        self.assertIn("<th>Имя</th>", content)
        self.assertIn("<th>Дата создания</th>", content)
        self.assertIn(data["status"]["name"], content)

        # Update and Delete links
        self.assertIn('<a href="/statuses/1/update/">Изменить</a>', content)
        self.assertIn('<a href="/statuses/1/delete/">Удалить</a>', content)


class TestStatusUpdate(TestStatusSetUp):
    def setUp(self) -> None:
        return super().setUp()

    def test_update_page_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        status_id = self.status.id

        response = self.client.get(
            reverse_lazy("update_status", kwargs={"id": status_id})
        )
        content = response.content.decode("utf-8")
        self.assertIn("Update status", content)
        self.assertIn("Name", content)
        self.assertIn(data["status"]["name"], content)

    def test_update_page_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})
        status_id = self.status.id

        response = self.client.get(
            reverse_lazy("update_status", kwargs={"id": status_id})
        )
        content = response.content.decode("utf-8")
        self.assertIn("Изменение статуса", content)
        self.assertIn("Имя", content)
        self.assertIn(data["status"]["name"], content)


class TestStatusCreate(TestStatusSetUp):
    def setUp(self) -> None:
        return super().setUp()

    def test_create_page_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})

        response = self.client.get(reverse_lazy("create_status"))
        content = response.content.decode("utf-8")
        self.assertIn("Create status", content)
        self.assertIn("Name", content)

    def test_create_page_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        response = self.client.get(reverse_lazy("create_status"))
        content = response.content.decode("utf-8")
        self.assertIn("Создать статус", content)
        self.assertIn("Имя", content)
