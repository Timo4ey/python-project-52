# from django.contrib import admin
from django.urls import path

import task_manager.main.views as views
import task_manager.users.views as views_users

urlpatterns = [
    path("", views.IndexViews.as_view(), name="main"),
    path("login/", views_users.UserLoginView.as_view(), name="login"),
    path("logout/", views_users.UserLogOutView.as_view(), name="logout"),
]
