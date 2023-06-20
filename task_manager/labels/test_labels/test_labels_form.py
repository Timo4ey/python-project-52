from django.test import TransactionTestCase

from task_manager.labels.forms import FormLabel
from task_manager.tests.conftest import data


class TestCreateForm(TransactionTestCase):
    def test_label_form_is_valid(self):
        valid_form = FormLabel({"name": data["label"]["name"]})
        self.assertTrue(valid_form.is_valid())

    def test_label_form_min_characters(self):
        valid_form = FormLabel({"name": "a" * 100})
        self.assertTrue(valid_form.is_valid())

    def test_label_form_max_characters(self):
        self.assertTrue(FormLabel({"name": "a" * 100}).is_valid())

    def test_label_form_101_characters(self):
        self.assertFalse(FormLabel({"name": "a" * 101}).is_valid())

    def test_label_form_zero_characters(self):
        self.assertFalse(FormLabel({"name": ""}).is_valid())
