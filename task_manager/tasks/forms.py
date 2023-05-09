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
        # print(self.fields)
        # print(self.fields['executor'].__dict__)
        # print('\n')
        # print(self.fields['executor'].__dir__())
        # print(User.objects.values_list('first_name', 'last_name'))
        # self.fields['executor']._set_queryset()  #
        # print([u.get_full_name() for u in User.objects.all()])
        # print([(u.id, u.get_full_name()) for u in User.objects.all()])
        # print([(User.objects.get(id=u.id), u.get_full_name()) for u in User.objects.all()])
        # # self.fields['executor'].choices = executor_fields
        # self.fields['executor'] = forms.ChoiceField(choices=[(u, u.get_full_name()) for u in User.objects.all()])
        self.fields['executor'].label = self.display_executor
        self.fields['executor'].widget.attrs.update({
            'class': 'form-control',
            'title': '',
        })

        self.fields['labels'].label = self.display_label
        self.fields['labels'].widget.attrs.update({
            'class': 'form-control',
        })
