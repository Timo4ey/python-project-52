from django.contrib.messages.views import SuccessMessageMixin
from django.forms.forms import BaseForm
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.services import AuthorizationCheckMixin, TaskPermissionMixin
from task_manager.tasks.models import Tasks

from .filters import TaskFilter
from .forms import CreateTaskForm


class TasksIndexView(AuthorizationCheckMixin, FilterView):
    model = Tasks
    template_name = "tasks/index.html"
    filterset_class = TaskFilter
    filterset_fields = ["status", "executor", "labels", "creator"]
    context_object_name = "tasks"


class TasksPageView(AuthorizationCheckMixin, DetailView):
    model = Tasks
    pk_url_kwarg = "id"
    template_name = "tasks/task_page.html"


class CreateTasksView(
    AuthorizationCheckMixin, SuccessMessageMixin, CreateView
):
    model = Tasks
    form_class = CreateTaskForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks")
    success_message = _("Задача успешно создана")

    def form_valid(self, form: BaseForm) -> HttpResponse:
        form.instance.creator = self.request.user
        return super().form_valid(form)


class UpdateTasksView(
    AuthorizationCheckMixin, SuccessMessageMixin, UpdateView
):
    model = Tasks
    form_class = CreateTaskForm
    template_name = "tasks/update.html"
    success_message = _("Задача успешно изменена")
    context_object_name = "update_task"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("tasks")


class DeleteTasksView(
    AuthorizationCheckMixin,
    TaskPermissionMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = Tasks
    template_name = "tasks/delete.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("tasks")
    success_message = _("Задача успешно удалена")
