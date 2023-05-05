from django.contrib.auth.models import User
from django.test import TestCase


class TestModels(TestCase):
    def setUp(self) -> None:
        self.new_user = User.objects.create(username='test')

    def test_user_is_existed(self):
        self.assertEqual('test', self.new_user.username)
