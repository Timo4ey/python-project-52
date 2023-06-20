from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.users.models import User

ru_headers = {"intl.accept_languages": "ru"}


class TestTask(TestCase):
    def setUp(self) -> None:
        self.credentials = {"username": "testuser", "password": "secret"}
        User.objects.create_user(**self.credentials)

    def test_login_is_active_true(self):
        response = self.client.post(
            reverse_lazy("login"), self.credentials, follow=True
        )
        self.assertTrue(response.context["user"].is_active)

    def test_login_is_active_false(self):
        response = self.client.post(reverse_lazy("login"), self.credentials)
        self.assertFalse(response.context is True)
