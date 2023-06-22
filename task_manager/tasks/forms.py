from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Tasks


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = (
            "name",
            "description",
            "status",
            "executor",
            "labels",
        )

    def __init__(self, *args, **kwargs):
        super(CreateTaskForm, self).__init__(*args, **kwargs)

        self.fields["name"].label = _("Имя")
        self.fields["description"].label = _("Описание")
        self.fields["status"].label = _("Статус")
        self.fields["executor"].label = _("Исполнитель")
        self.fields["labels"].label = _("Метки")
