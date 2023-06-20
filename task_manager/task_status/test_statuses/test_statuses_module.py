from django.conf import settings
from django.contrib.messages import get_messages
from django.urls import reverse_lazy

from task_manager.task_status.models import TaskStatus
from task_manager.tests.conftest import TestStatusSetUp, TestUserSetUp, data


class TestsStatuses(TestUserSetUp):
    def test_statuses_page(self):
        response = self.client.get(reverse_lazy("statuses"))
        self.assertEqual(response.status_code, 200)


class TestsCreateStatus(TestStatusSetUp):
    def test_statuses_page_create(self):
        response = self.client.get(reverse_lazy("create_status"))
        self.assertEqual(response.status_code, 200)

    def test_statuses_create_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})

        response = self.client.post(
            reverse_lazy("create_status"), {"name": data["status"]["name1"]}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("statuses"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "Status has been created successfully")
        response2 = self.client.get(reverse_lazy("statuses"))
        self.assertIn(
            data["status"]["name1"], response2.content.decode("utf-8")
        )

    def test_statuses_create_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        response = self.client.post(
            reverse_lazy("create_status"), {"name": data["status"]["name1"]}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("statuses"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "Статус успешно создан")

    def test_statuses_create_existed_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        response = self.client.post(
            reverse_lazy("create_status"), {"name": data["status"]["name"]}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Status is already exist",
            str(response.context["form"]),
        )

    def test_statuses_create_existed_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        response = self.client.post(
            reverse_lazy("create_status"), {"name": data["status"]["name"]}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Статус с таким название уже сущуствует",
            str(response.context["form"]),
        )


class TestsDeleteStatus(TestStatusSetUp):
    def test_statuses_delete_page(self):
        status = TaskStatus.objects.create(name=data["status"]["name1"])
        status.save()

        response = self.client.get(
            reverse_lazy("delete_status", kwargs={"id": status.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_statuses_delete_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        response = self.client.post(
            reverse_lazy("delete_status", kwargs={"id": self.status.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("statuses"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "Status has been deleted successfully")
        response2 = self.client.get(reverse_lazy("statuses"))
        self.assertNotIn(
            data["status"]["name"], response2.content.decode("utf-8")
        )

    def test_statuses_delete_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        response = self.client.post(
            reverse_lazy("delete_status", kwargs={"id": self.status.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("statuses"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "Статус успешно удален")


class TestsUpdateStatus(TestUserSetUp):
    def test_update_status_page(self):
        status = TaskStatus.objects.create(name=data["status"]["name"])
        status.save()
        response = self.client.get(
            reverse_lazy("update_status", kwargs={"id": status.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_update_status_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})

        status = TaskStatus.objects.create(name=data["status"]["name"])
        status.save()
        response = self.client.post(
            reverse_lazy("update_status", kwargs={"id": status.id}),
            {"name": data["status"]["name1"]},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("statuses"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "Status has been updated successfully")
        response2 = self.client.get(reverse_lazy("statuses"))
        self.assertIn(
            data["status"]["name1"], response2.content.decode("utf-8")
        )

    def test_update_status_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        status = TaskStatus.objects.create(name=data["status"]["name"])
        status.save()
        response = self.client.post(
            reverse_lazy("update_status", kwargs={"id": status.id}),
            {"name": data["status"]["name1"]},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("statuses"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "Статус успешно изменен")
