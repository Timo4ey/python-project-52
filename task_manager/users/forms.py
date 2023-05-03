from django import forms
from django.utils.safestring import mark_safe

from task_manager.users import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label=_('Имя'), max_length=150,  widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First name'}))

    second_name = forms.CharField(label=_('Фамилия'), max_length=150,  widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Second name'}))

    class Meta:
        model = User
        fields = ('first_name', 'second_name', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"class": 'form-control',
                                                     "placeholder": _('Имя пользователя'),
                                                     "label": _('Имя пользователя'),

                                                     })
        self.fields['username'].label = _('Имя пользователя')
        self.fields['username'].help_text = f'<small class="form-text text-muted">{_("Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.")}</small>'

        self.fields['password1'].widget.attrs.update({"class": 'form-control',
                                                      "placeholder": _('Пароль'),
                                                      "label": _('Пароль'),
                                                      "min_size": 3,

                                                      })
        self.fields['password1'].label = _('Пароль')
        self.fields['password1'].help_text = f'<small class="form-text text-muted"><ul>{_("Ваш пароль должен содержать как минимум 3 символа.")}</ul></small>'
        print()

        self.fields['password2'].widget.attrs.update({"class": 'form-control',
                                                     "placeholder": _('Подтверждение пароля'),
                                                     "label": _('Пароль'),
                                                      })
        self.fields['password2'].label = _('Подтверждение пароля')
        self.fields['password2'].help_text = f'<small class="form-text text-muted">{_("Для подтверждения введите, пожалуйста, пароль ещё раз.")}</small>'


class UserLogingForm(forms.ModelForm):

    class Meta:
        model = models.User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"class": '',
                                                     "placeholder": _('Имя пользователя'),
                                                     "label": _('Имя пользователя'),

                                                     })
        self.fields['password'].widget.attrs.update({"class": '',
                                                     "placeholder": _('Пароль'),
                                                     "label": _('Пароль'),
                                                     })

# class UserRegistrationForm(UserCreationForm):
#
#     class Meta:
#         model = models.User
#         fields = ('first_name', 'second_name', 'username', 'password1', 'password2')
#         help_texts = {
#             "username": _("Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_."),
#             "password1": _("Ваш пароль должен содержать как минимум 3 символа.")
#         }
#         localized_fields = (_(x) for x in fields)
#
#     def __init__(self, *args, **kwargs):
#         super(UserCreationForm, self).__init__(*args, **kwargs)
#
#         self.fields['first_name'].widget.attrs.update({"class": '',
#                                                        "placeholder": _('Имя'),
#                                                        "label": _('Имя'),
#                                                        })
#         self.fields['second_name'].widget.attrs.update({"class": '',
#                                                        "placeholder": _('Фамилия'),
#                                                         "label": _('Фамилия'),
#                                                         })
#         self.fields['username'].widget.attrs.update({"class": '',
#                                                      "placeholder": _('Имя пользователя'),
#                                                      "label": _('Имя пользователя'),
#
#                                                      })
#         self.fields['password1'].widget.attrs.update({"class": '',
#                                                       "placeholder": _('Пароль'),
#                                                       "label": _('Пароль'),
#                                                       "min_size": 3,
#
#                                                       })
#
#         self.fields['password1'].help_text = f"{_('Ваш пароль должен содержать как минимум 3 символа.')}"
#         self.fields['password2'].widget.attrs.update({"class": '',
#                                                      "placeholder": _('Подтверждение пароля'),
#                                                      "label": _('Пароль'),
#                                                       })
#         self.fields['password2'].help_text = _("Для подтверждения введите, пожалуйста, пароль ещё раз.")


# class UserRegistrationForm(UserCreationForm):
#     first_name = forms.CharField(max_length=150)
#
#     class Meta:
#         model = models.User
#         fields = ('first_name', 'second_name', 'username', 'password1', 'password2')
#         widgets = {
#             'password': forms.PasswordInput(attrs={'class': ''},
#                                             )
#         }
#         help_texts = {
#             "username": _("Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.")
#             , "password": _("Ваш пароль должен содержать как минимум 3 символа.")
#         }
#         localized_fields = (_(x) for x in fields)
#
#     def __init__(self, *args, **kwargs):
#         super(UserCreationForm, self).__init__(*args, **kwargs)
#
#         self.fields['first_name'].widget.attrs.update({"class": '',
#                                                        "placeholder": _('Имя'),
#                                                        "label": _('Имя'),
#                                                        })
#         self.fields['second_name'].widget.attrs.update({"class": '',
#                                                        "placeholder": _('Фамилия'),
#                                                         "label": _('Фамилия'),
#                                                         })
#         self.fields['username'].widget.attrs.update({"class": '',
#                                                      "placeholder": _('Имя пользователя'),
#                                                      "label": _('Имя пользователя'),
#
#                                                      })
#         self.fields['password1'].widget.attrs.update({"class": '',
#                                                      "placeholder": _('Пароль'),
#                                                      "label": _('Пароль'),
#                                                      })
#         self.fields['password2'].widget.attrs.update({"class": '',
#                                                      "placeholder": _('Пароль'),
#                                                      "label": _('Пароль'),
#                                                      })



# class UserRegistrationForm(forms.ModelForm):
#     password2 = forms.CharField(widget=forms.PasswordInput())
#
#     class Meta:
#         model = models.User
#         fields = ['first_name', 'second_name', 'username', 'password', 'password2']
#         widgets = {
#             'password': forms.PasswordInput(attrs={'class': ''},
#                                             )
#         }
#         help_texts = {
#             "username": _("Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.")
#             , "password": _("Ваш пароль должен содержать как минимум 3 символа.")
#         }
#         localized_fields = (_(x) for x in fields)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['first_name'].widget.attrs.update({"class": '',
#                                                        "placeholder": _('Имя'),
#                                                        "label": _('Имя'),
#                                                        })
#         self.fields['second_name'].widget.attrs.update({"class": '',
#                                                        "placeholder": _('Фамилия'),
#                                                         "label": _('Фамилия'),
#                                                         })
#         self.fields['username'].widget.attrs.update({"class": '',
#                                                      "placeholder": _('Имя пользователя'),
#                                                      "label": _('Имя пользователя'),
#
#                                                      })
#         self.fields['password'].widget.attrs.update({"class": '',
#                                                      "placeholder": _('Пароль'),
#                                                      "label": _('Пароль'),
#                                                      })
#
#         self.fields['password2'].widget.attrs.update({"class": '',
#                                                      "placeholder": _('Подтверждение пароля'),
#                                                      "label": _('Подтверждение пароля'),
#                                                      })