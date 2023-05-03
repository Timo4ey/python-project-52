from django import forms

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class UserLogingForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(UserLogingForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"class": '',
                                                     "placeholder": _('Имя пользователя'),
                                                     "label": _('Имя пользователя'),

                                                     })

        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs.update({"class": '',
                                                     "placeholder": _('Пароль'),
                                                     "label": _('Пароль'),
                                                     })
