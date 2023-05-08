from django import forms
from .models import Tasks
from django.utils.translation import gettext_lazy as _


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['name', 'description',
                  'status', 'performer', 'labels']
        exclude = ('creator',)

    def __init__(self, *args, **kwargs):
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        self.display_name = _('Имя')
        self.display_description = _('Описание')
        self.display_status = _('Статус')
        self.display_performer = _('Исполнитель')
        self.display_tags = _('Метки')

        # self.fields['creator'].label = 'Создатель'
        # self.fields['creator'].widget = self.fields['creator'].hidden_widget()
        # self.fields['creator'].widget.attrs.update({
        #     'class': 'form-control',
        # })

        self.fields['name'].label = self.display_name
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': self.display_name
        })

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': self.display_description,
            'label':  self.display_description,
        })

        self.fields['status'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': self.display_status,
            'label': self.display_status,
        })

        self.fields['performer'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': self.display_performer,
            'label': self.display_performer,
        })

        self.fields['labels'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': self.display_tags,
            'label': self.display_tags,
        })
