from django.conf import settings
from django.test import modify_settings
from django.urls import reverse_lazy

from task_manager.labels.models import Label
from task_manager.tests.conftest import TestLabelSetUp, data


@modify_settings(
    MIDDLEWARE={
        "remove": [
            "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
        ]
    }
)
class TestLabelsIndexPage(TestLabelSetUp):
    def test_empty_main_page(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        label = Label.objects.get(name=data["label"]["name"])
        label.delete()

        response = self.client.get(reverse_lazy("labels"))
        content = response.content.decode("utf-8")
        self.assertNotIn('<a href="/labels/1/update/">Изменить</a>', content)
        self.assertNotIn('<a href="/labels/1/delete/">Удалить</a>', content)

    def test_main_page_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        response = self.client.get(reverse_lazy("labels"))
        content = response.content.decode("utf-8")
        # h1
        self.assertIn('<h1 class="my-4">Labels</h1>', content)
        # Table
        self.assertIn("<th>ID</th>", content)
        self.assertIn("<th>Name</th>", content)
        self.assertIn("<th>Created at</th>", content)
        self.assertIn(data["label"]["name"], content)

        # Update link
        self.assertIn('<a href="/labels/1/update/">Update</a>', content)
        self.assertIn('<a href="/labels/1/delete/">Delete</a>', content)

    def test_main_page_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})
        response = self.client.get(reverse_lazy("labels"))
        content = response.content.decode("utf-8")
        # h1
        self.assertIn('<h1 class="my-4">Метки</h1>', content)
        # Table
        self.assertIn("<th>ID</th>", content)
        self.assertIn("<th>Имя</th>", content)
        self.assertIn("<th>Дата создания</th>", content)
        self.assertIn(data["label"]["name"], content)

        # Update and Delete links
        self.assertIn('<a href="/labels/1/update/">Изменить</a>', content)
        self.assertIn('<a href="/labels/1/delete/">Удалить</a>', content)


class TestLabelsUpdate(TestLabelSetUp):
    def setUp(self) -> None:
        return super().setUp()

    def test_update_page_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        label_id = self.label.id

        response = self.client.get(
            reverse_lazy("update_label", kwargs={"id": label_id})
        )
        content = response.content.decode("utf-8")
        self.assertIn("Change label", content)
        self.assertIn("Name", content)
        self.assertIn(data["label"]["name"], content)

    def test_update_page_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})
        label_id = self.label.id

        response = self.client.get(
            reverse_lazy("update_label", kwargs={"id": label_id})
        )
        content = response.content.decode("utf-8")
        self.assertIn("Изменение метки", content)
        self.assertIn("Имя", content)
        self.assertIn(data["label"]["name"], content)


class TestLabelsCreate(TestLabelSetUp):
    def setUp(self) -> None:
        return super().setUp()

    def test_update_page_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})

        response = self.client.get(reverse_lazy("create_label"))
        content = response.content.decode("utf-8")
        self.assertIn("Create label", content)
        self.assertIn("Name", content)

    def test_update_page_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        response = self.client.get(reverse_lazy("create_label"))
        content = response.content.decode("utf-8")
        self.assertIn("Создать Метку", content)
        self.assertIn("Имя", content)
