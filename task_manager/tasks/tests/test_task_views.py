from datetime import datetime as dt

from django.conf import settings
from django.urls import reverse_lazy

from task_manager.labels.models import Label
from task_manager.task_status.models import TaskStatus
from task_manager.tests.conftest import TestUserLabelStatusSetUP
from task_manager.users.models import User


class TestTasksViews(TestUserLabelStatusSetUP):
    def test_main_tasks_page_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})
        response = self.client.get(reverse_lazy("tasks"))
        content = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn('<table class="table table-striped">', content)
        self.assertIn('<h1 class="my-4">Задачи</h1>', content)

        self.assertIn("<th>ID</th>", content)
        self.assertIn("<th>Имя</th>", content)
        self.assertIn("<th>Статус</th>", content)
        self.assertIn("<th>Автор</th>", content)
        self.assertIn("<th>Исполнитель</th>", content)
        self.assertIn("<th>Дата создания</th>", content)

        self.assertIn(str(self.task.id), content)
        self.assertIn(self.task.name, content)
        self.assertIn(self.task.status.name, content)
        self.assertIn(self.task.creator.get_full_name(), content)
        self.assertIn(self.task.executor.get_full_name(), content)
        self.assertIn(
            f'<a href="/tasks/{self.task.id}/update/">Изменить</a>', content
        )
        self.assertIn(
            f'<a href="/tasks/{self.task.id}/delete/">Удалить</a>', content
        )

    def test_main_tasks_page_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        response = self.client.get(reverse_lazy("tasks"))
        content = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn('<table class="table table-striped">', content)
        self.assertIn('<h1 class="my-4">Tasks</h1>', content)

        self.assertIn("<th>ID</th>", content)
        self.assertIn("<th>Name</th>", content)
        self.assertIn("<th>Status</th>", content)
        self.assertIn("<th>Author</th>", content)
        self.assertIn("<th>Executor</th>", content)
        self.assertIn("<th>Created at</th>", content)

        self.assertIn(str(self.task.id), content)
        self.assertIn(self.task.name, content)
        self.assertIn(self.task.status.name, content)
        self.assertIn(self.task.creator.get_full_name(), content)
        self.assertIn(self.task.executor.get_full_name(), content)
        self.assertIn(
            f'<a href="/tasks/{self.task.id}/update/">Update</a>', content
        )
        self.assertIn(
            f'<a href="/tasks/{self.task.id}/delete/">Delete</a>', content
        )


class TestTasksViewsCreate(TestUserLabelStatusSetUP):
    def test_create_tasks_page_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        response = self.client.get(reverse_lazy("create_task"))
        content = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)

        self.assertIn(str(self.task.id), content)
        self.assertIn('<h1 class="my-4">Create task</h1>', content)

        self.assertIn('<label for="id_name">Name</label>', content)
        self.assertIn(
            '<label for="id_description">Description</label>', content
        )
        self.assertIn('<label for="id_status">Status</label>', content)
        self.assertIn('<label for="id_executor">Executor</label>', content)
        self.assertIn('<label for="id_labels">Labels</label>', content)
        self.assertIn(
            '<input class="btn btn-primary" type="submit" value="Create">',
            content,
        )
        for label in list(Label.objects.all().values_list("name", flat=True)):
            self.assertIn(label, content)
        for status in list(
            TaskStatus.objects.all().values_list("name", flat=True)
        ):
            self.assertIn(status, content)
        executor_list = [x.get_full_name() for x in User.objects.all()]
        for user_full_name in executor_list:
            self.assertIn(user_full_name, content)

    def test_create_tasks_page_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})
        response = self.client.get(reverse_lazy("create_task"))
        content = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)

        self.assertIn(str(self.task.id), content)
        self.assertIn('<h1 class="my-4">Создать задачу</h1>', content)

        self.assertIn('<label for="id_name">Имя</label>', content)
        self.assertIn('<label for="id_description">Описание</label>', content)
        self.assertIn('<label for="id_status">Статус</label>', content)
        self.assertIn('<label for="id_executor">Исполнитель</label>', content)
        self.assertIn('<label for="id_labels">Метки</label>', content)
        self.assertIn(
            '<input class="btn btn-primary" type="submit" value="Создать">',
            content,
        )

        for label in list(Label.objects.all().values_list("name", flat=True)):
            self.assertIn(label, content)
        for status in list(
            TaskStatus.objects.all().values_list("name", flat=True)
        ):
            self.assertIn(status, content)
        executor_list = [x.get_full_name() for x in User.objects.all()]
        for user_full_name in executor_list:
            self.assertIn(user_full_name, content)


class TestTasksViewsUpdate(TestUserLabelStatusSetUP):
    def test_update_tasks_page_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        response = self.client.get(
            reverse_lazy("update_task", kwargs={"id": self.task.id})
        )
        content = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)

        self.assertIn(str(self.task.id), content)
        self.assertIn(self.task.name, content)
        self.assertIn(self.task.description, content)
        self.assertIn(self.task.status.name, content)
        self.assertIn(self.task.executor.get_full_name(), content)
        self.assertIn(str(self.task.id), content)

        self.assertIn('<h1 class="my-4">Update task</h1>', content)

        self.assertIn('<label for="id_name">Name</label>', content)
        self.assertIn(
            '<label for="id_description">Description</label>', content
        )
        self.assertIn('<label for="id_status">Status</label>', content)
        self.assertIn('<label for="id_executor">Executor</label>', content)
        self.assertIn('<label for="id_labels">Labels</label>', content)
        self.assertIn(
            '<input class="btn btn-primary" type="submit" value="Update">',
            content,
        )
        for label in list(Label.objects.all().values_list("name", flat=True)):
            self.assertIn(label, content)
        for status in list(
            TaskStatus.objects.all().values_list("name", flat=True)
        ):
            self.assertIn(status, content)
        executor_list = [x.get_full_name() for x in User.objects.all()]
        for user_full_name in executor_list:
            self.assertIn(user_full_name, content)

    def test_update_tasks_page_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})
        response = self.client.get(
            reverse_lazy("update_task", kwargs={"id": self.task.id})
        )
        content = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)

        self.assertIn(str(self.task.id), content)
        self.assertIn(self.task.name, content)
        self.assertIn(self.task.description, content)
        self.assertIn(self.task.status.name, content)
        for assign_label in list(
            self.task.labels.values_list("name", flat=True)
        ):
            self.assertIn(assign_label, content)

        self.assertIn(self.task.executor.get_full_name(), content)

        self.assertIn('<h1 class="my-4">Изменить задачу</h1>', content)

        self.assertIn('<label for="id_name">Имя</label>', content)
        self.assertIn('<label for="id_description">Описание</label>', content)
        self.assertIn('<label for="id_status">Статус</label>', content)
        self.assertIn('<label for="id_executor">Исполнитель</label>', content)
        self.assertIn('<label for="id_labels">Метки</label>', content)
        self.assertIn(
            '<input class="btn btn-primary" type="submit" value="Изменить">',
            content,
        )
        for label in list(Label.objects.all().values_list("name", flat=True)):
            self.assertIn(label, content)
        for status in list(
            TaskStatus.objects.all().values_list("name", flat=True)
        ):
            self.assertIn(status, content)
        executor_list = [x.get_full_name() for x in User.objects.all()]
        for user_full_name in executor_list:
            self.assertIn(user_full_name, content)


class TestTasksViewsDelete(TestUserLabelStatusSetUP):
    def test_delete_tasks_page_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        response = self.client.get(
            reverse_lazy("delete_task", kwargs={"id": self.task.id})
        )
        content = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)

        self.assertIn('<h1 class="my-4">Delete task</h1>', content)

        self.assertIn(
            f"<p>Are you sure that you want to delete {self.task.name}?</p>",
            content,
        )

        self.assertIn(
            '<input class="btn btn-danger" type="submit" value="Yes, delete">',
            content,
        )

    def test_delete_tasks_page_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})
        response = self.client.get(
            reverse_lazy("delete_task", kwargs={"id": self.task.id})
        )
        content = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)

        self.assertIn('<h1 class="my-4">Удаление Задачи</h1>', content)

        self.assertIn(
            f"<p>Вы уверены, что хотите удалить {self.task.name}?</p>",
            content,
        )

        self.assertIn(
            '<input class="btn btn-danger" type="submit" value="Да, удалить">',
            content,
        )


class TestTasksViewsTasksPage(TestUserLabelStatusSetUP):
    def test_tasks_page_tasks_page_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        response = self.client.get(
            reverse_lazy("page_task", kwargs={"id": self.task.id})
        )
        content = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)

        self.assertIn('<h1 class="my-4">Task view</h1>', content)
        self.assertIn(f"<h2>{self.task.name}</h2>", content)
        self.assertIn(f"<p>{self.task.description}</p>", content)
        self.assertIn(
            f'<div class="col">{self.task.creator.get_full_name()}</div>',
            content,
        )
        self.assertIn(f'<div class="col">{self.task.executor}</div>', content)
        self.assertIn(f'<div class="col">{self.task.status}</div>', content)
        date = dt.strftime(
            dt.fromtimestamp(self.task.created_at.timestamp()),
            "%d.%m.%Y %H:%m",
        )

        self.assertIn(f'<div class="col">{date}</div>', content)
        for label in list(self.task.labels.values_list("name", flat=True)):
            self.assertIn(f"<li>{label}</li>", content)
        self.assertIn(
            f'<a href="/tasks/{self.task.id}/update/">Update</a>', content
        )
        self.assertIn(
            f'<a href="/tasks/{self.task.id}/delete/">Delete</a>', content
        )

    def test_tasks_page_tasks_page_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})
        response = self.client.get(
            reverse_lazy("page_task", kwargs={"id": self.task.id})
        )
        content = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)

        self.assertIn('<h1 class="my-4">Просмотр задачи</h1>', content)
        self.assertIn(f"<h2>{self.task.name}</h2>", content)
        self.assertIn(f"<p>{self.task.description}</p>", content)
        self.assertIn(
            f'<div class="col">{self.task.creator.get_full_name()}</div>',
            content,
        )
        self.assertIn(f'<div class="col">{self.task.executor}</div>', content)
        self.assertIn(f'<div class="col">{self.task.status}</div>', content)
        date = dt.strftime(
            dt.fromtimestamp(self.task.created_at.timestamp()),
            "%d.%m.%Y %H:%m",
        )

        self.assertIn(f'<div class="col">{date}</div>', content)
        for label in list(self.task.labels.values_list("name", flat=True)):
            self.assertIn(f"<li>{label}</li>", content)
        self.assertIn(
            f'<a href="/tasks/{self.task.id}/update/">Изменить</a>', content
        )
        self.assertIn(
            f'<a href="/tasks/{self.task.id}/delete/">Удалить</a>', content
        )
