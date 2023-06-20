from django.test import modify_settings

from task_manager.labels.models import Label
from task_manager.tasks.models import Tasks
from task_manager.tests.conftest import TestUserLabelStatusSetUP, data


@modify_settings(
    MIDDLEWARE={
        "remove": [
            "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
        ]
    }
)
class TestTaskModel(TestUserLabelStatusSetUP):
    def test_creation_full(self):
        tasks = Tasks.objects.create(
            **{
                "creator": self.user,
                "name": data["tasks"]["task"]["name"],
                "description": data["tasks"]["task"]["description"],
                "status": self.status,
                "executor": self.user,
            }
        )
        tasks.labels.set(Label.objects.filter(name=self.label.name))
        tasks.save()
        self.assertEqual(tasks.creator, self.user)
        self.assertEqual(tasks.name, data["tasks"]["task"]["name"])
        self.assertEqual(
            tasks.description, data["tasks"]["task"]["description"]
        )
        self.assertEqual(tasks.status, self.status)
        self.assertEqual(tasks.executor, self.user)
        self.assertEqual(self.label.name, tasks.labels.values_list()[0][1])

    def test_model_another_executor(self):
        tasks = Tasks.objects.create(
            **{
                "creator": self.user,
                "name": data["tasks"]["task"]["name"],
                "description": data["tasks"]["task"]["description"],
                "status": self.status,
                "executor": self.user2,
            }
        )
        tasks.save()
        self.assertEqual(tasks.executor.username, self.user2.username)
