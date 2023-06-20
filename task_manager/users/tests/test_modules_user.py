from django.conf import settings
from django.contrib.messages import get_messages
from django.test import modify_settings
from django.urls import reverse_lazy

from task_manager.tests.conftest import TestUserSetUp, data
from task_manager.users.models import User


@modify_settings(
    MIDDLEWARE={
        "remove": [
            "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
        ]
    }
)
class TestUserCreation(TestUserSetUp):
    s = "Password is too short. Passport must contain at least 3 characters."

    def test_create_user_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})
        response = self.client.post(
            reverse_lazy("create_user"),
            {
                "first_name": data["user1"]["first_name"],
                "last_name": data["user1"]["last_name"],
                "username": data["user1"]["username"],
                "password1": data["user1"]["password1"],
                "password2": data["user1"]["password2"],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("login"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)

        message_str = str(messages[0])

        self.assertEqual(message_str, "Пользователь успешно зарегистрирован")

    def test_user_already_exist_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})
        response = self.client.post(
            reverse_lazy("create_user"),
            {
                "first_name": data["user"]["first_name"],
                "last_name": data["user"]["last_name"],
                "username": data["user"]["username"],
                "password1": data["user"]["password1"],
                "password2": data["user"]["password2"],
            },
        )
        self.assertEqual(response.status_code, 400)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)

        self.assertIn(
            "Пользователь с таким именем уже существует.",
            str(response.context["form"]),
        )

    def test_create_user_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        response = self.client.post(
            reverse_lazy("create_user"),
            {
                "first_name": data["user1"]["first_name"],
                "last_name": data["user1"]["last_name"],
                "username": data["user1"]["username"],
                "password1": data["user1"]["password1"],
                "password2": data["user1"]["password2"],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("login"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)

        message_str = str(messages[0])

        self.assertEqual(message_str, "User has been registered successfully")

    def test_user_already_exist_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        response = self.client.post(
            reverse_lazy("create_user"),
            {
                "first_name": data["user"]["first_name"],
                "last_name": data["user"]["last_name"],
                "username": data["user"]["username"],
                "password1": data["user"]["password1"],
                "password2": data["user"]["password2"],
            },
        )
        self.assertEqual(response.status_code, 400)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)

        self.assertIn(
            "A user with that username already exists.",
            str(response.context["form"]),
        )

    def test_mismatch_password_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        response = self.client.post(
            reverse_lazy("create_user"),
            {
                "first_name": data["user1"]["first_name"],
                "last_name": data["user1"]["last_name"],
                "username": data["user1"]["username"],
                "password1": data["user"]["password1"],
                "password2": data["user1"]["password2"],
            },
        )
        self.assertEqual(response.status_code, 400)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)

        self.assertIn(
            "Password mismatch",
            str(response.context["form"]),
        )

    def test_mismatch_password_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})
        response = self.client.post(
            reverse_lazy("create_user"),
            {
                "first_name": data["user1"]["first_name"],
                "last_name": data["user1"]["last_name"],
                "username": data["user1"]["username"],
                "password1": data["user"]["password1"],
                "password2": data["user1"]["password2"],
            },
        )
        self.assertEqual(response.status_code, 400)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)

        self.assertIn(
            "Введенные пароли не совпадают.",
            str(response.context["form"]),
        )

    def test_short_password_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})

        response = self.client.post(
            reverse_lazy("create_user"),
            {
                "first_name": data["user1"]["first_name"],
                "last_name": data["user1"]["last_name"],
                "username": data["user1"]["username"],
                "password1": data["short_password"],
                "password2": data["short_password"],
            },
        )
        self.assertEqual(response.status_code, 400)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)

        self.assertIn(
            self.s,
            str(response.context["form"]),
        )

    def test_short_password_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})
        response = self.client.post(
            reverse_lazy("create_user"),
            {
                "first_name": data["user1"]["first_name"],
                "last_name": data["user1"]["last_name"],
                "username": data["user1"]["username"],
                "password1": data["short_password"],
                "password2": data["short_password"],
            },
        )
        self.assertEqual(response.status_code, 400)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)

        self.assertIn(
            "Введённый пароль слишком короткий.",
            str(response.context["form"]),
        )

    def test_user_login(self):
        user = User.objects.get(username=data["user"]["username"])
        self.assertTrue(user.is_active)

    def test_user_login_show_bars(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        response = self.client.get(reverse_lazy("users"))
        self.assertEqual(response.status_code, 200)

        self.assertIn("Users", response.content.decode("utf-8"))
        self.assertIn("Tasks", response.content.decode("utf-8"))
        self.assertIn("Statuses", response.content.decode("utf-8"))
        self.assertIn("Labels", response.content.decode("utf-8"))

    def test_user_logout_pages_tasks_labels_statuses(self):
        self.client.logout()

        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})

        response = self.client.get(reverse_lazy("tasks"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse_lazy("labels"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse_lazy("statuses"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse_lazy("login"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse_lazy("create_user"))
        self.assertEqual(response.status_code, 200)

    def test_user_logout_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        response = self.client.get(reverse_lazy("logout"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(messages, "Вы разлогинены")

    def test_user_logout_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})

        response = self.client.get(reverse_lazy("logout"))
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(messages, "You logout")


class TestUpdateUser(TestUserSetUp):
    def test_upd_page_is_available(self):
        response = self.client.get(
            reverse_lazy("update_user", kwargs={"id": self.user.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data["user"]["first_name"])
        self.assertContains(response, data["user"]["last_name"])
        self.assertContains(response, data["user"]["username"])

    def test_upd_page_logout_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        self.client.logout()

        response = self.client.get(
            reverse_lazy("update_user", kwargs={"id": self.user.id})
        )
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            messages, "Вы не авторизованы! Пожалуйста, выполните вход."
        )

    def test_upd_page_logout_en(self):
        self.client.logout()
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})

        response = self.client.get(
            reverse_lazy("update_user", kwargs={"id": self.user.id})
        )
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(messages, "You aren't authorized! Please, login.")

    def test_upd_user_not_exits(self):
        response = self.client.get(
            reverse_lazy("update_user", kwargs={"id": self.user.id + 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users"))

    def test_change_username(self):
        response = self.client.post(
            reverse_lazy("update_user", kwargs={"id": self.user.id}),
            {
                "first_name": data["user"]["first_name"],
                "last_name": data["user"]["last_name"],
                "username": data["user_update"]["username"],
                "password1": data["user"]["password1"],
                "password2": data["user"]["password2"],
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse_lazy("users"))
        self.assertContains(response, data["user_update"]["username"])

    def test_change_first_name(self):
        response = self.client.post(
            reverse_lazy("update_user", kwargs={"id": self.user.id}),
            {
                "first_name": data["user_update"]["first_name"],
                "last_name": data["user"]["last_name"],
                "username": data["user"]["username"],
                "password1": data["user"]["password1"],
                "password2": data["user"]["password2"],
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse_lazy("users"))
        self.assertContains(response, data["user_update"]["first_name"])

    def test_change_last_name(self):
        response = self.client.post(
            reverse_lazy("update_user", kwargs={"id": self.user.id}),
            {
                "first_name": data["user"]["first_name"],
                "last_name": data["user_update"]["last_name"],
                "username": data["user"]["username"],
                "password1": data["user"]["password1"],
                "password2": data["user"]["password2"],
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse_lazy("users"))
        self.assertContains(response, data["user_update"]["last_name"])

    def test_username_is_already_exist_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})

        User.objects.create(
            **{
                "first_name": data["user1"]["first_name"],
                "last_name": data["user1"]["last_name"],
                "username": data["user1"]["username"],
            }
        )

        response = self.client.post(
            reverse_lazy("update_user", kwargs={"id": self.user.id}),
            {
                "first_name": data["user"]["first_name"],
                "last_name": data["user"]["last_name"],
                "username": data["user1"]["username"],
                "password1": data["user"]["password1"],
                "password2": data["user"]["password2"],
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            data["user1"]["username"], response.content.decode("utf-8")
        )
        self.assertIn(
            "A user with that username already exists.",
            str(response.context["form"]),
        )

    def test_username_is_already_exist_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        second_user = User.objects.create(
            **{
                "first_name": data["user1"]["first_name"],
                "last_name": data["user1"]["last_name"],
                "username": data["user1"]["username"],
            }
        )
        second_user.save()

        response = self.client.post(
            reverse_lazy("update_user", kwargs={"id": self.user.id}),
            {
                "first_name": data["user"]["first_name"],
                "last_name": data["user"]["last_name"],
                "username": data["user1"]["username"],
                "password1": data["user"]["password1"],
                "password2": data["user"]["password2"],
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            data["user1"]["username"], response.content.decode("utf-8")
        )
        self.assertIn(
            "Пользователь с таким именем уже существует.",
            str(response.context["form"]),
        )

    def test_update_another_user_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        second_user = User.objects.create(
            **{
                "first_name": data["user1"]["first_name"],
                "last_name": data["user1"]["last_name"],
                "username": data["user1"]["username"],
            }
        )
        second_user.set_password(data["user1"]["password1"])
        second_user.save()

        response = self.client.get(
            reverse_lazy("update_user", kwargs={"id": second_user.id})
        )
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users"))
        self.assertEqual(
            messages, "У вас нет прав для изменения другого пользователя."
        )

    def test_update_another_user_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})

        second_user = User.objects.create(
            **{
                "first_name": data["user1"]["first_name"],
                "last_name": data["user1"]["last_name"],
                "username": data["user1"]["username"],
            }
        )
        second_user.set_password(data["user1"]["password1"])
        second_user.save()

        response = self.client.get(
            reverse_lazy("update_user", kwargs={"id": second_user.id})
        )
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users"))
        self.assertEqual(
            messages, "You don't have rights to change another user."
        )

    def test_update_another_user_logout_en(self):
        self.client.logout()
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        response = self.client.get(
            reverse_lazy("update_user", kwargs={"id": self.user.id})
        )
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("login"))
        self.assertEqual(messages, "You aren't authorized! Please, login.")

    def test_update_another_user_logout_ru(self):
        self.client.logout()
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})
        response = self.client.get(
            reverse_lazy("update_user", kwargs={"id": self.user.id})
        )
        messages = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("login"))
        self.assertEqual(
            messages, "Вы не авторизованы! Пожалуйста, выполните вход."
        )


class TestUserDelete(TestUserSetUp):
    def test_delete_user_page(self):
        response = self.client.get(
            reverse_lazy("delete_user", kwargs={"id": self.user.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_user_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        response = self.client.post(
            reverse_lazy("delete_user", kwargs={"id": self.user.id})
        )
        messages = str(list(get_messages(response.wsgi_request))[0])

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users"))
        self.assertEqual(messages, "Пользователь успешно удалён")
        response2 = self.client.get(reverse_lazy("users"))
        self.assertNotIn(
            data["user"]["username"], response2.content.decode("utf-8")
        )

    def test_delete_another_user_ru(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})
        second_user = User.objects.create(
            **{
                "first_name": data["user1"]["first_name"],
                "last_name": data["user1"]["last_name"],
                "username": data["user1"]["username"],
            }
        )
        second_user.set_password(data["user1"]["password1"])
        second_user.save()

        response = self.client.post(
            reverse_lazy("delete_user", kwargs={"id": second_user.id})
        )
        messages = str(list(get_messages(response.wsgi_request))[0])

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users"))
        self.assertEqual(
            messages, "У вас нет прав для изменения другого пользователя."
        )
        response2 = self.client.get(reverse_lazy("users"))
        self.assertIn(
            data["user"]["username"], response2.content.decode("utf-8")
        )

    def test_delete_another_user_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})
        second_user = User.objects.create(
            **{
                "first_name": data["user1"]["first_name"],
                "last_name": data["user1"]["last_name"],
                "username": data["user1"]["username"],
            }
        )
        second_user.set_password(data["user1"]["password1"])
        second_user.save()

        response = self.client.post(
            reverse_lazy("delete_user", kwargs={"id": second_user.id})
        )
        messages = str(list(get_messages(response.wsgi_request))[0])

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users"))
        self.assertEqual(
            messages, "You don't have rights to change another user."
        )
        response2 = self.client.get(reverse_lazy("users"))
        self.assertIn(
            data["user"]["username"], response2.content.decode("utf-8")
        )

    def test_delete_user_en(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})

        response = self.client.post(
            reverse_lazy("delete_user", kwargs={"id": self.user.id})
        )
        messages = str(list(get_messages(response.wsgi_request))[0])

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users"))
        self.assertEqual(messages, "User has been deleted successfully")

    def test_delete_user_unregistered_ru(self):
        self.client.logout()
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})

        response = self.client.get(
            reverse_lazy("delete_user", kwargs={"id": self.user.id})
        )
        messages = str(list(get_messages(response.wsgi_request))[0])

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("login"))
        self.assertEqual(
            messages, "Вы не авторизованы! Пожалуйста, выполните вход."
        )

    def test_delete_user_unregistered_en(self):
        self.client.logout()
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en-us"})

        response = self.client.get(
            reverse_lazy("delete_user", kwargs={"id": self.user.id})
        )
        messages = str(list(get_messages(response.wsgi_request))[0])

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("login"))
        self.assertEqual(messages, "You aren't authorized! Please, login.")
