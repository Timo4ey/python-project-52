from django import forms
from django.utils.translation import gettext_lazy as _

from .models import TaskStatus


class FormTaskStatus(forms.ModelForm):
    class Meta:
        model = TaskStatus
        fields = ("name",)

    label_place = _("Имя")

    def __init__(self, *args, **kwargs):
        super(FormTaskStatus, self).__init__(*args, **kwargs)
        self.fields["name"].label = self.label_place
        self.fields["name"].help_text = None
        self.fields["name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": self.label_place,
            }
        )

    def clean_name(self):
        name = self.cleaned_data["name"]
        if TaskStatus.objects.filter(name=name):
            raise forms.ValidationError(
                _("Статус с таким название уже сущуствует")
            )
        return name
