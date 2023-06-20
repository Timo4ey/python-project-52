from django.conf import settings
from django.db.models.deletion import ProtectedError
from django.test import modify_settings
from django.urls import reverse_lazy

from task_manager.tests.conftest import TestUserLabelStatusSetUP


@modify_settings(
    MIDDLEWARE={
        "remove": [
            "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
        ]
    }
)
class TestForbiddenToDelete(TestUserLabelStatusSetUP):
    def test_delete_user_if_it_has_task_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        try:
            self.client.post(
                reverse_lazy("delete_user", kwargs={"id": self.user.id})
            )
        except ProtectedError as er:
            self.assertIn("Cannot delete some instances of model", er.args[0])

    def test_delete_status_if_it_has_task_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        try:
            self.client.post(
                reverse_lazy("delete_status", kwargs={"id": self.status.id})
            )
        except ProtectedError as er:
            self.assertIn("Cannot delete some instances of model", er.args[0])
