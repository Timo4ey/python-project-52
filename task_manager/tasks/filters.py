import django_filters
from django import forms
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Concat
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.task_status.models import TaskStatus

from .models import Tasks


class TaskFilter(django_filters.FilterSet):
    STATUSES_CHOICE = TaskStatus.objects.all().values_list("id", "name")
    PERFORMER_CHOICE = User.objects.annotate(
        full_name=Concat("first_name", Value(" "), "last_name")
    ).values_list("id", "full_name")
    LABELS_CHOICE = Label.objects.all().values_list("id", "name")

    creator = django_filters.BooleanFilter(
        label=_("Только свои задачи"),
        method="my_custom_filter",
        widget=forms.CheckboxInput,
    )
    status = django_filters.ChoiceFilter(
        label=_("Статус"), choices=STATUSES_CHOICE
    )
    labels = django_filters.ChoiceFilter(
        label=_("Метка"), choices=LABELS_CHOICE
    )
    executor = django_filters.ChoiceFilter(
        label=_("Исполнитель"), choices=PERFORMER_CHOICE
    )

    class Meta:
        model = Tasks
        fields = ["status", "executor", "labels", "creator"]

    #
    def __init__(self, *args, **kwargs):
        super(TaskFilter, self).__init__(*args, **kwargs)
        self.user_id = self.request.user.id

    def my_custom_filter(self, queryset, value):
        if value:
            return queryset.filter(creator_id=self.user_id)
        return queryset
