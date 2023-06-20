# from django.contrib import admin
from django.urls import path

import task_manager.main.views as views

urlpatterns = [
    path("", views.IndexViews.as_view(), name="main"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogOutView.as_view(), name="logout"),
]
