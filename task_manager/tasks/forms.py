from django import forms

from .models import Tasks
from django.utils.translation import gettext_lazy as _


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['name', 'description',
                  'status', 'executor', 'labels']
        exclude = ('creator',)

    def __init__(self, *args, **kwargs):
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        self.display_name = _('Имя')
        self.display_description = _('Описание')
        self.display_status = _('Статус')
        self.display_executor = _('Исполнитель')
        self.display_label = _('Метки')

        self.fields['name'].label = self.display_name
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': self.display_name,
        })

        self.fields['description'].label = self.display_description
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': self.display_description,
        })

        self.fields['status'].label = self.display_status
        self.fields['status'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['executor'].label = self.display_executor
        self.fields['executor'].widget.attrs.update({
            'class': 'form-control',
            'title': '',
        })

        self.fields['labels'].label = self.display_label
        self.fields['labels'].widget.attrs.update({
            'class': 'form-control',
        })
