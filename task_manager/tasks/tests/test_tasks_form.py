from django.conf import settings
from django.contrib.messages import get_messages
from django.test import modify_settings
from django.urls import reverse_lazy

from task_manager.tests.conftest import TestUserLabelStatusSetUP, data


@modify_settings(
    MIDDLEWARE={
        "remove": [
            "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
        ]
    }
)
class TestTaskCreate(TestUserLabelStatusSetUP):
    def test_create_task_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        response = self.client.post(
            reverse_lazy("create_task"),
            {
                "name": data["tasks"]["task"]["name"],
                "description": data["tasks"]["task"]["description"],
                "status": self.status.id,
                "executor": self.user.id,
                "labels": self.label.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("tasks"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "The task has been added successfully")

    def test_create_task_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})
        response = self.client.post(
            reverse_lazy("create_task"),
            {
                "name": data["tasks"]["task"]["name"],
                "description": data["tasks"]["task"]["description"],
                "status": self.status.id,
                "executor": self.user.id,
                "labels": self.label.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("tasks"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "Задача успешно создана")

    def test_create_task_assign_another_user(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        response = self.client.post(
            reverse_lazy("create_task"),
            {
                "name": data["tasks"]["task"]["name"],
                "description": data["tasks"]["task"]["description"],
                "status": self.status.id,
                "executor": self.user2.id,
                "labels": self.label.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("tasks"))

    def test_create_task_same_name_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        self.client.post(
            reverse_lazy("create_task"),
            {
                "name": data["tasks"]["task"]["name"],
                "description": data["tasks"]["task"]["description"],
                "status": self.status.id,
                "executor": self.user2.id,
                "labels": self.label.id,
            },
        )
        response = self.client.post(
            reverse_lazy("create_task"),
            {
                "name": data["tasks"]["task"]["name"],
                "description": data["tasks"]["task"]["description"],
                "status": self.status.id,
                "executor": self.user2.id,
                "labels": self.label,
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Tasks with this Name already exists.",
            str(response.context["form"]),
        )


class TestTaskUpdate(TestUserLabelStatusSetUP):
    def test_update_task_page_is_available(self):
        response = self.client.get(
            reverse_lazy("update_task", kwargs={"id": self.task.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_update_task_page_change_fields(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        response = self.client.post(
            reverse_lazy("update_task", kwargs={"id": self.task.id}),
            {
                "creator": self.user.id,
                "executor": 1,
                "status": 2,
                "name": "New name",
                "description": data["tasks"]["task1"]["description"] + "!!!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("tasks"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "Задача успешно изменена")

    def test_update_task_page_change_fields_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})

        response = self.client.post(
            reverse_lazy("update_task", kwargs={"id": self.task.id}),
            {
                "creator": self.user.id,
                "executor": 1,
                "status": 2,
                "name": "New name",
                "description": data["tasks"]["task1"]["description"] + "!!!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("tasks"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "The task has been changed")

    def test_update_task_name_exits_name_is_failed(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})

        response = self.client.post(
            reverse_lazy("update_task", kwargs={"id": self.task.id}),
            {
                "name": data["tasks"]["task2"]["name"],
                "description": data["tasks"]["task"]["description"],
                "status": self.status.id,
                "executor": self.user2.id,
                "labels": self.label,
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Tasks with this Name already exists.",
            str(response.context["form"]),
        )


class TestTaskDelete(TestUserLabelStatusSetUP):
    def test_delete_task_page_is_available(self):
        response = self.client.get(
            reverse_lazy("delete_task", kwargs={"id": self.task.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_task_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        response = self.client.post(
            reverse_lazy("delete_task", kwargs={"id": self.task.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("tasks"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "Задача успешно удалена")

    def test_delete_task_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})

        response = self.client.post(
            reverse_lazy("delete_task", kwargs={"id": self.task.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("tasks"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "The task has been deleted")

    def test_cant_delete_another_users_task_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        response = self.client.post(
            reverse_lazy("delete_task", kwargs={"id": self.task2.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("tasks"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "Задачу может удалить только её автор")

    def test_cant_delete_another_users_task_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})

        response = self.client.post(
            reverse_lazy("delete_task", kwargs={"id": self.task2.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("tasks"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(messages, "The task can delete only its author")


class TestTaskFilter(TestUserLabelStatusSetUP):
    def test_get_task_with_specific_data_status(self):
        url = reverse_lazy("tasks") + f"?status={self.task.status.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertIn(f"selected>{self.task.status.name}", content)

    def test_get_task_with_specific_data_label(self):
        label_id = list(self.task.labels.values_list("id", flat=True))
        label_name = list(self.task.labels.values_list("name", flat=True))
        url = reverse_lazy("tasks") + f"?labels={label_id[0]}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertIn(f"selected>{label_name[0]}", content)

    def test_get_task_with_specific_data_executor(self):
        url = reverse_lazy("tasks") + f"?executor={self.task.executor.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertIn(
            f"selected>{self.task.executor.get_full_name()}", content
        )

    def test_get_task_with_specific_data_label_and_status(self):
        label_id = list(self.task.labels.values_list("id", flat=True))
        label_name = list(self.task.labels.values_list("name", flat=True))
        add_string = f"?labels={label_id[0]}&status={self.task.status.id}"
        url = reverse_lazy("tasks") + add_string
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertIn(f"selected>{label_name[0]}", content)
        self.assertIn(f"selected>{self.task.status.name}", content)

    def test_get_task_with_specific_data_label_and_status_and_creator(self):
        label_id = list(self.task.labels.values_list("id", flat=True))
        label_name = list(self.task.labels.values_list("name", flat=True))
        labels = f"labels={label_id[0]}"
        status = f"status={self.task.status.id}"
        executor = f"executor={self.task.executor.id}"
        add_string = f"?{labels}&{status}&{executor}"
        url = reverse_lazy("tasks") + add_string
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertIn(f"selected>{label_name[0]}", content)
        self.assertIn(f"selected>{self.task.status.name}", content)
        self.assertIn(
            f"selected>{self.task.executor.get_full_name()}", content
        )

    def test_get_task_with_specific_data_label_and_status_and_creator_on(self):
        label_id = list(self.task.labels.values_list("id", flat=True))
        label_name = list(self.task.labels.values_list("name", flat=True))
        labels = f"labels={label_id[0]}"
        status = f"status={self.task.status.id}"
        executor = f"executor={self.task.executor.id}"
        add_string = f"?{labels}&{status}&{executor}&creator=on"
        url = reverse_lazy("tasks") + add_string
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertIn(f"selected>{label_name[0]}", content)
        self.assertIn(f"selected>{self.task.status.name}", content)
        self.assertIn(
            f"selected>{self.task.executor.get_full_name()}", content
        )
