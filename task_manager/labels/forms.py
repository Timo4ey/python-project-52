from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Label


class FormLabel(forms.ModelForm):
    class Meta:
        model = Label
        fields = ("name",)

    label_place = _("Имя")

    def __init__(self, *args, **kwargs):
        super(FormLabel, self).__init__(*args, **kwargs)
        self.fields["name"].label = self.label_place

    def clean_name(self):
        name = self.cleaned_data["name"]
        if Label.objects.filter(name=name):
            raise forms.ValidationError(
                _("Метка с таким названием уже сущуствует")
            )
        return name
