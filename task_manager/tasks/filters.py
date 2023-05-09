import django_filters
from django.contrib.auth.models import User

from .models import Tasks
from task_manager.task_status.models import TaskStatus
from task_manager.labels.models import Label
from django import forms
from django.utils.translation import gettext_lazy as _


class F(django_filters.FilterSet):
    STATUSES_CHOICE = TaskStatus.objects.all().values_list('id', 'name')
    PERFORMER_CHOICE = [(x.id, x.get_full_name()) for x in User.objects.all()]
    STATUSES_TAGS = Label.objects.all().values_list('id', 'name')

    creator = django_filters.BooleanFilter(label=_("Только свои задачи"), method='my_custom_filter',
                                           widget=forms.CheckboxInput)
    status = django_filters.ChoiceFilter(label=_("Статус"), choices=STATUSES_CHOICE)
    labels = django_filters.ChoiceFilter(label=_("Метка"), choices=STATUSES_TAGS)
    executor = django_filters.ChoiceFilter(label=_("Исполнитель"), choices=PERFORMER_CHOICE)

    class Meta:
        model = Tasks
        fields = ['status', 'executor', 'labels', 'creator']

    #
    def __init__(self,  *args, **kwargs):
        super(F, self).__init__(*args, **kwargs)
        self.user_id = self.request.user.id

    def my_custom_filter(self, queryset, field, value, *args, **kwargs):
        if value:
            return queryset.filter(creator_id=self.user_id)
        return queryset
