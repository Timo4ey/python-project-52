from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):

    first_name = forms.CharField(label=_('Имя'), max_length=150,
                                 widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': 'First name'}))

    last_name = forms.CharField(label=_('Фамилия'), max_length=150,
                                widget=forms.TextInput(
                                attrs={'class': 'form-control', 'placeholder': 'Second name'}))

    username_help_text = _("Обязательное поле. Не более 150 символов.\
                            Только буквы, цифры и символы @/./+/-/_.")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"class": 'form-control',
                                                     "placeholder": _('Имя пользователя'),
                                                     "label": _('Имя пользователя'),

                                                     })
        self.fields['username'].label = _('Имя пользователя')
        self.fields['username'].help_text = self.username_help_text

        self.fields['password1'].widget.attrs.update({"class": 'form-control',
                                                      "placeholder": _('Пароль'),
                                                      "label": _('Пароль'),
                                                      "min_size": 3,

                                                      })
        self.fields['password1'].label = _('Пароль')
        self.fields['password1'].help_text = f'{_("Ваш пароль должен содержать как минимум 3 символа.")}'

        self.fields['password2'].widget.attrs.update({"class": 'form-control',
                                                      "placeholder": _('Подтверждение пароля'),
                                                      "label": _('Пароль'),
                                                      })
        self.fields['password2'].label = _('Подтверждение пароля')
        self.fields['password2'].help_text = _("Для подтверждения введите, пожалуйста, пароль ещё раз.")

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError(_('Введенные пароли не совпадают.'))
        if len(password2) < 3:
            raise ValidationError(_('Введённый пароль слишком короткий.\
             Он должен содержать как минимум 3 символа.'))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise ValidationError(_('Пользователь с таким именем уже существует.'))
        return username


class UpdateForm(UserChangeForm):
    # form =
    first_name = forms.CharField(label=_('Имя'), max_length=150,
                                 widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': 'First name'}))

    last_name = forms.CharField(label=_('Фамилия'), max_length=150,
                                widget=forms.TextInput(
                                attrs={'class': 'form-control', 'placeholder': 'Second name'}))

    username_help_text = _("Обязательное поле. Не более 150 символов.\
                            Только буквы, цифры и символы @/./+/-/_.")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
                                attrs={'class': 'form-control', 'placeholder': 'Second name'}),)
    password2 = forms.CharField(label="Password", widget=forms.PasswordInput(
                                attrs={'class': 'form-control', 'placeholder': 'Second name'}),)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')  #

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"class": 'form-control',
                                                     "placeholder": _('Имя пользователя'),
                                                     "label": _('Имя пользователя'),

                                                     })
        print(self.fields['username'].__dict__)
        self.fields['username'].validators = [MaxLengthValidator]
        self.fields['username'].label = _('Имя пользователя')
        self.fields['username'].help_text = self.username_help_text

        self.fields['password1'].widget.attrs.update({"class": 'form-control',
                                                      "placeholder": _('Пароль'),
                                                      "label": _('Пароль'),
                                                      "min_size": 3,

                                                      })
        self.fields['password1'].label = _('Пароль')
        self.fields['password1'].help_text = f'{_("Ваш пароль должен содержать как минимум 3 символа.")}'

        self.fields['password2'].widget.attrs.update({"class": 'form-control',
                                                      "placeholder": _('Подтверждение пароля'),
                                                      "label": _('Пароль'),
                                                      })
        self.fields['password2'].label = _('Подтверждение пароля')
        self.fields['password2'].help_text = _("Для подтверждения введите, пожалуйста, пароль ещё раз.")

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError(_('Введенные пароли не совпадают.'))
        if len(password2) < 3:
            raise ValidationError(_('Введённый пароль слишком короткий.\
             Он должен содержать как минимум 3 символа.'))


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
