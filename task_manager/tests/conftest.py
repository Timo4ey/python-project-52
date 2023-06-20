import os
from json import loads
from pathlib import Path

from django.test import TestCase, modify_settings

from task_manager.labels.models import Label
from task_manager.task_status.models import TaskStatus
from task_manager.tasks.models import Tasks
from task_manager.users.models import User


def get_file_data(file_name):
    with open(os.path.join(Path(__file__).parent, file_name), "r") as f:
        return loads(f.read())[0]


data = get_file_data("test_data_user.json")


@modify_settings(
    MIDDLEWARE={
        "remove": [
            "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
        ]
    }
)
class TestUserSetUp(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            **{
                "first_name": data["user"]["first_name"],
                "last_name": data["user"]["last_name"],
                "username": data["user"]["username"],
            }
        )
        self.user.set_password(data["user"]["password1"])
        self.user.save()

        self.client.login(
            **{
                "username": data["user"]["username"],
                "password": data["user"]["password1"],
            },
            follow=True,
        )


class TestStatusSetUp(TestUserSetUp):
    def setUp(self) -> None:
        self.status = TaskStatus.objects.create(name=data["status"]["name"])
        self.status.save()
        return super().setUp()


class TestLabelSetUp(TestUserSetUp):
    def setUp(self) -> None:
        self.label = Label.objects.create(name=data["label"]["name"])
        self.label.save()
        return super().setUp()


@modify_settings(
    MIDDLEWARE={
        "remove": [
            "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
        ]
    }
)
class TestUserLabelStatusSetUP(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            **{
                "first_name": data["user"]["first_name"],
                "last_name": data["user"]["last_name"],
                "username": data["user"]["username"],
            }
        )
        self.user.set_password(data["user"]["password1"])
        self.user.save()

        self.client.login(
            **{
                "username": data["user"]["username"],
                "password": data["user"]["password1"],
            },
            follow=True,
        )
        self.status = TaskStatus.objects.create(name=data["status"]["name"])
        self.status.save()
        self.label = Label.objects.create(name=data["label"]["name"])
        self.label.save()
        self.user2 = User.objects.create(username=data["user1"]["username"])
        self.user2.save()

        self.status2 = TaskStatus.objects.create(name=data["status"]["name1"])
        self.status2.save()
        self.label2 = Label.objects.create(name=data["label"]["name1"])
        self.label2.save()
        self.task = Tasks.objects.create(
            creator=self.user,
            executor=self.user2,
            status=self.status,
            **data["tasks"]["task1"],
        )
        self.task.labels.set((self.label.id,))
        self.task.save()

        self.task2 = Tasks.objects.create(
            creator=self.user2,
            executor=self.user,
            status=self.status2,
            **data["tasks"]["task2"],
        )
        self.task.labels.set((self.label.id,))
        self.task.save()
