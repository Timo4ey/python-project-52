from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView, ListView, UpdateView

from task_manager.services import (
    AuthorizationCheckMixin,
    LabelStatusCreateMixin,
    LabelStatusesPermissionMixin,
)

from .forms import FormLabel
from .models import Label

# Create your views here.


class IndexViews(AuthorizationCheckMixin, ListView):
    model = Label
    template_name = "label/index.html"
    context_object_name = "labels"


class LabelCreateView(LabelStatusCreateMixin):
    model = Label
    form_class = FormLabel
    template_name = "label/create.html"
    success_url = reverse_lazy("labels")
    success_message = _("Метка успешно создана")


class LabelUpdateView(
    AuthorizationCheckMixin, SuccessMessageMixin, UpdateView
):
    model = Label
    form_class = FormLabel
    template_name = "label/update.html"
    pk_url_kwarg = "id"
    success_message = _("Метка успешно изменена")
    success_url = reverse_lazy("labels")


class LabelDeleteView(
    AuthorizationCheckMixin,
    SuccessMessageMixin,
    LabelStatusesPermissionMixin,
    DeleteView,
):
    model = Label
    template_name = "label/delete.html"
    success_message = _("Метка успешно удалена")
    pk_url_kwarg = "id"
    success_url = reverse_lazy("labels")
