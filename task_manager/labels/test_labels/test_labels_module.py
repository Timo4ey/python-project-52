from django.conf import settings
from django.contrib.messages import get_messages
from django.test import modify_settings
from django.urls import reverse_lazy

from task_manager.labels.models import Label
from task_manager.tests.conftest import TestLabelSetUp, TestUserSetUp, data


@modify_settings(
    MIDDLEWARE={
        "remove": [
            "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
        ]
    }
)
class TestsLabels(TestUserSetUp):
    def test_labels_page(self):
        response = self.client.get(reverse_lazy("labels"))
        self.assertEqual(response.status_code, 200)


class TestsCreateLabel(TestLabelSetUp):
    def test_labels_page_create(self):
        response = self.client.get(reverse_lazy("create_label"))
        self.assertEqual(response.status_code, 200)

    def test_labels_create_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})

        response = self.client.post(
            reverse_lazy("create_label"), {"name": data["label"]["name1"]}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("labels"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "Label has been created successfully")
        response2 = self.client.get(reverse_lazy("labels"))
        self.assertIn(data["label"]["name"], response2.content.decode("utf-8"))

    def test_labels_create_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        response = self.client.post(
            reverse_lazy("create_label"), {"name": data["label"]["name1"]}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("labels"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "Метка успешно создана")

    def test_labels_create_existed_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        response = self.client.post(
            reverse_lazy("create_label"), {"name": data["label"]["name"]}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Label is already exist",
            str(response.context["form"]),
        )

    def test_labels_create_existed_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        response = self.client.post(
            reverse_lazy("create_label"), {"name": data["label"]["name"]}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Метка с таким названием уже сущуствует",
            str(response.context["form"]),
        )


class TestsDeleteLabel(TestLabelSetUp):
    def test_labels_delete_page(self):
        label = Label.objects.create(name=data["label"]["name1"])
        label.save()

        response = self.client.get(
            reverse_lazy("delete_label", kwargs={"id": label.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_labels_delete_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        response = self.client.post(
            reverse_lazy("delete_label", kwargs={"id": self.label.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("labels"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "Label has been deleted successfully")
        response2 = self.client.get(reverse_lazy("labels"))
        self.assertNotIn(
            data["label"]["name"], response2.content.decode("utf-8")
        )

    def test_labels_delete_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        response = self.client.post(
            reverse_lazy("delete_label", kwargs={"id": self.label.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("labels"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "Метка успешно удалена")


class TestsUpdateLabel(TestUserSetUp):
    def test_update_label_page(self):
        label = Label.objects.create(name=data["label"]["name"])
        label.save()
        response = self.client.get(
            reverse_lazy("update_label", kwargs={"id": label.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_update_label_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})

        label = Label.objects.create(name=data["label"]["name"])
        label.save()
        response = self.client.post(
            reverse_lazy("update_label", kwargs={"id": label.id}),
            {"name": data["label"]["name1"]},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("labels"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "Label has been updated successfully")
        response2 = self.client.get(reverse_lazy("labels"))
        self.assertIn(
            data["label"]["name1"], response2.content.decode("utf-8")
        )

    def test_update_label_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        label = Label.objects.create(name=data["label"]["name1"])
        label.save()
        response = self.client.post(
            reverse_lazy("update_label", kwargs={"id": label.id}),
            {"name": data["label"]["name1"]},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("labels"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "Метка успешно изменена")
