from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.services import (
    AuthorizationCheckMixin,
    LabelStatusesPermissionMixin,
)

from .forms import FormTaskStatus
from .models import TaskStatus

# Create your views here.


class IndexViews(AuthorizationCheckMixin, ListView):
    model = TaskStatus
    template_name = "status/index.html"
    context_object_name = "statuses"


class StatusCreateView(
    AuthorizationCheckMixin, SuccessMessageMixin, CreateView
):
    model = TaskStatus
    form_class = FormTaskStatus
    template_name = "status/create.html"
    success_url = reverse_lazy("statuses")
    success_message = _("Статус успешно создан")


class StatusUpdateView(
    AuthorizationCheckMixin, SuccessMessageMixin, UpdateView
):
    model = TaskStatus
    template_name = "status/update.html"
    form_class = FormTaskStatus
    pk_url_kwarg = "id"
    success_message = _("Статус успешно изменен")
    success_url = reverse_lazy("statuses")


class StatusDeleteView(
    AuthorizationCheckMixin,
    SuccessMessageMixin,
    LabelStatusesPermissionMixin,
    DeleteView,
):
    model = TaskStatus
    template_name = "status/delete.html"
    pk_url_kwarg = "id"
    success_message = _("Статус успешно удален")
    success_url = reverse_lazy("statuses")
