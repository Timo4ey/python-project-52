from django.test import TestCase

from task_manager.labels.models import Label
from task_manager.tests.conftest import data


class TestLabelModel(TestCase):
    def test_valid_input(self):
        label = Label.objects.create(name=data["label"]["name"])
        self.assertEqual(data["label"]["name"], label.name)

    def test_valid_input_min(self):
        label = Label.objects.create(name="s")
        self.assertEqual("s", label.name)

    def test_valid_input_max(self):
        label = Label.objects.create(name="s" * 100)
        self.assertEqual("s" * 100, label.name)
