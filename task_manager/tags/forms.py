from django import forms
from .models import Tags
from django.utils.translation import gettext_lazy as _


class FormTag(forms.ModelForm):
    class Meta:
        model = Tags
        fields = 'name',

    label_place = _('Имя')

    def __init__(self, *args, **kwargs):
        super(FormTag, self).__init__(*args, **kwargs)
        self.fields['name'].label = self.label_place
        self.fields['name'].help_text = None
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            "placeholder": self.label_place,
        }
        )
