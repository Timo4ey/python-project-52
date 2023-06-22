from typing import Any

from django import http
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import ValidationError
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Tasks
from task_manager.users.models import User


class LabelStatusesPermissionMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        pattern = self.find_pattern(self)
        if self.kwargs.get("id") in list(
            Tasks.objects.all().values_list(
                "labels" if pattern == "label" else "status", flat=True
            )
        ):
            return False
        return True

    def handle_no_permission(self) -> HttpResponseRedirect:
        pattern = self.find_pattern(self)

        if self.raise_exception or self.request.user.is_authenticated:
            messages.error(
                self.request, self.chose_error(self.find_pattern(self))
            )
            return redirect(
                reverse_lazy("statuses" if pattern == "status" else "labels")
            )
        return super().handle_no_permission()

    def find_pattern(self, *args, **kwargs):
        ans: str = ""
        if (
            self.request.__dict__.get("resolver_match").url_name.find("label")
            != -1
        ):
            ans = "label"

        if (
            self.request.__dict__.get("resolver_match").url_name.find("status")
            != -1
        ):
            ans = "status"
        return ans

    def chose_error(self, pattern: str):
        return {
            "status": _(
                "Невозможно удалить статус, потому что он используется"
            ),
            "label": _(
                "Невозможно удалить метку, потому что она используется"
            ),
        }.get(pattern)


class UserPermissionMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        if self.request.user.id != self.kwargs.get("id"):
            return False
        return True

    def handle_no_permission(self) -> HttpResponseRedirect:
        if self.raise_exception or self.request.user.is_authenticated:
            messages.error(
                self.request,
                _("У вас нет прав для изменения другого пользователя."),
            )
            return redirect(reverse_lazy("users"))
        return super().handle_no_permission()


class AuthorizationCheckMixin(LoginRequiredMixin):
    redirect_url = reverse_lazy("login")
    permission_denied_message = _(
        "Вы не авторизованы! Пожалуйста, выполните вход."
    )
    redirect_field_name = None

    def get_login_url(self) -> str:
        print("!", self.request.GET)
        messages.error(self.request, self.permission_denied_message)
        print(self.request.GET)
        return str(self.redirect_url)


class ErrorMessageMixin:
    error_message = _("Оба поля могут быть чувствительны к регистру.")

    def dispatch(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse:
        print(self.is_not_correct_password())

        if self.is_not_zero_len() and self.is_request_post_name_is_not_none():
            messages.add_message(request, messages.ERROR, self.error_message)
        elif (
            self.is_not_correct_password() is False
            and self.is_request_post_name_is_not_none()
        ):
            messages.add_message(request, messages.ERROR, self.error_message)

        response = super().dispatch(request, *args, **kwargs)
        return response

    def is_not_zero_len(self):
        return (
            len(
                list(
                    User.objects.filter(
                        username=self.request.POST.get("username")
                    )
                )
            )
            == 0
        )

    def is_request_post_name_is_not_none(self):
        return self.request.POST.get("username") is not None

    def is_not_correct_password(self):
        if self.is_not_zero_len() is False:
            print("!!!")
            return User.objects.get(
                username=self.request.POST.get("username")
            ).check_password(self.request.POST.get("password"))
        return False


class TaskPermissionMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        print(self.find_task_creator(self))
        print(self.request.user.id)
        if self.request.user.id != self.find_task_creator(self):
            return False
        return True

    def handle_no_permission(self) -> HttpResponseRedirect:
        if self.raise_exception or self.request.user.is_authenticated:
            messages.error(
                self.request,
                _("Задачу может удалить только ее автор"),
            )
            return redirect(reverse_lazy("tasks"))
        return super().handle_no_permission()

    def find_task_creator(self, *args, **kwargs):
        task = Tasks.objects.filter(id=self.kwargs.get("id"))
        if len(task) == 0:
            raise ValidationError("Tasks matching query does not exist.")
        return task[0].creator.id
