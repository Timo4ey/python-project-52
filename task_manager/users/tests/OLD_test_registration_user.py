# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from django.urls import reverse, reverse_lazy
# from task_manager.users.models import User
# import os
# from pathlib import Path
# from json import loads
# from django.test import RequestFactory, TestCase


# def get_file_data(file_name):
#     with open(os.path.join(Path(__file__).parent, file_name), "r") as f:
#         return loads(f.read())[0]


# data = get_file_data("test_data_user.json")


# class TestTask(StaticLiveServerTestCase):
#     def setUp(self) -> None:
#         self.create_url = reverse("create_user")
#         self.factory = RequestFactory()
#         # self.update_user = reverse('update_user')
#         # self.delete_user = reverse('delete_user')

#     def test_status_200_create_user_page(self):
#         response = self.client.get(self.create_url)
#         assert response.status_code == 200

#     def test_create_user(self):
#         self.client.post(
#             self.create_url,
#             {
#                 "first_name": data["user"]["first_name"],
#                 "last_name": data["user"]["last_name"],
#                 "username": data["user"]["username"],
#                 "password1": data["user"]["password1"],
#                 "password2": data["user"]["password2"],
#             },
#             follow=True,
#         )
#         users_page = self.client.get(reverse("users"))
#         content = users_page.content.decode("utf-8")
#         self.assertIn(data["user"]["first_name"], content)
#         self.assertIn(data["user"]["last_name"], content)
#         self.assertIn(data["user"]["username"], content)

#     def test_update_user_page_status_200(self):
#         response = self.client.post(
#             self.create_url,
#             {
#                 "first_name": data["user"]["first_name"],
#                 "last_name": data["user"]["last_name"],
#                 "username": data["user"]["username"],
#                 "password1": data["user"]["password1"],
#                 "password2": data["user"]["password2"],
#             },
#             follow=True,
#         )
#         user = User.objects.get(username=data["user"]["username"])
#         response.get(reverse("update_user", kwargs={"id": user.id}))
#         assert response.status_code == 200

#     def test_update_user_name(self):
#         User.objects.create(
#             **{
#                 "first_name": data["user"]["first_name"],
#                 "last_name": data["user"]["last_name"],
#                 "username": data["user"]["username"],
#                 "password": data["user"]["password1"],
#             },
#         )
#         user = User.objects.get(username=data["user"]["username"])
#         # response.client.[p]
#         response = self.client.post(
#             reverse("login"),
#             {
#                 "username": data["user"]["username"],
#                 "password": data["user"]["password1"],
#             },
#             follow=True,
#         )
#         self.client.get(f"users/{user.id}/update/")

#         # response.client.post(
#         #     f"users/{user.id}/update/",
#         #     {
#         #         "first_name": "fdsfs",
#         #         "last_name": data["user"]["last_name"],
#         #         "username": data["user"]["username"],
#         #         "password1": data["user"]["password1"],
#         #         "password2": data["user"]["password2"],
#         #     },
#         #     follow=True,
#         # )

#         # # self.assertEqual(response.status_code, 302)
#         # self.assertEqual(response.status_code, 200)
#         # # users_page = response.client.get(reverse("users"))
#         # # content = users_page.content.decode("utf-8")
#         # user.refresh_from_db()
#         # self.assertIn(
#         #     "Пользователь успешно изменён", user.first_name
#         # )

#     # def test_upd(self):
#     #     request = self.factory.get(reverse("users"))
#     #     assert request.status_code == 200


# # from task_manager.users.views import UserFormCreateView


# # class TestUserFab(TestCase):
# #     def setUp(self):
# #         # Every test needs access to the request factory.
# #         self.factory = RequestFactory()
# #         # self.user = User.objects.create_user(
# #         #     username="jacob", email="jacob@…", password="top_secret"
# #         # )

# #     def test_reg_user(self):
# #         request = self.factory.get(
# #             reverse("create_user"),
# #         )
# #         response = UserFormCreateView().as_view(request)
# #         self.assertEqual(response.status_code, 200)
