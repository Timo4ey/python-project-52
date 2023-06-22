from typing import Any

from django import http
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.services import (
    AuthorizationCheckMixin,
    ErrorMessageMixin,
    UserPermissionMixin,
)
from task_manager.users.forms import SignUpForm, UpdateForm

from .forms import UserLoginForm


class IndexUser(ListView):
    model = User
    template_name = "users/users.html"
    context_object_name = "users"


class UserFormCreateView(SuccessMessageMixin, CreateView):
    template_name = "users/create.html"
    form_class = SignUpForm
    redirect_authenticated_user = True
    success_message = _("Пользователь успешно зарегистрирован")
    success_url = reverse_lazy("login")


class UserUpdateView(
    AuthorizationCheckMixin,
    UserPermissionMixin,
    UpdateView,
    SuccessMessageMixin,
):
    model = User
    template_name = "users/update.html"
    form_class = UpdateForm
    pk_url_kwarg = "id"
    success_message = _("Пользователь успешно изменен")
    success_url = reverse_lazy("users")


class UserDeleteView(
    AuthorizationCheckMixin,
    UserPermissionMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = User
    template_name = "users/delete.html"
    pk_url_kwarg = "id"
    success_message = _("Пользователь успешно удален")
    success_url = reverse_lazy("users")


class UserLoginView(SuccessMessageMixin, ErrorMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = "login.html"
    fields = ["username", "password"]
    redirect_authenticated_user = True
    success_message = _("Вы залогинены")

    def get_success_url(self) -> str:
        return reverse_lazy("main")


class UserLogOutView(SuccessMessageMixin, LogoutView):
    template_name = "index.html"

    def dispatch(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse:
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, _("Вы разлогинены"))
        return response

    def get_success_url(self) -> str | None:
        return reverse_lazy("main")
