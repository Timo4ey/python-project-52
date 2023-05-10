from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):

    first_name = forms.CharField(label=_('Имя'), max_length=150,
                                 widget=forms.TextInput(
                                 attrs={
                                     'class': 'form-control',
                                     'placeholder': _('Имя')}))

    last_name = forms.CharField(label=_('Фамилия'), max_length=150,
                                widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'placeholder': _('Фамилия')}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'password1',
                  'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {
                "class": 'form-control',
                "placeholder": _('Имя пользователя'),
                "label": _('Имя пользователя'),
            }
        )
        self.fields['username'].label = _('Имя пользователя')

        self.fields['password1'].widget.attrs.update(
            {
                "class": 'form-control',
                "placeholder": _('Пароль'),
                "label": _('Пароль'),
                "min_size": 3,

                                                      })
        self.fields['password1'].label = _('Пароль')
        self.fields['password1'].help_text =\
            f'{_("Ваш пароль должен содержать как минимум 3 символа.")}'

        self.fields['password2'].widget.attrs.update(
            {
                "class": 'form-control',
                "placeholder": _('Подтверждение пароля'),
                "label": _('Пароль'),
            }
        )
        self.fields['password2'].label = _('Подтверждение пароля')
        self.fields['password2'].help_text = _(
            "Для подтверждения введите, пожалуйста, пароль ещё раз.")

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
            raise ValidationError(
                _('Пользователь с таким именем уже существует.'))
        return username


class UpdateForm(UserChangeForm):
    first_name = forms.CharField(label=_('Имя'), max_length=150,
                                 widget=forms.TextInput(
                                 attrs={
                                     'class': 'form-control',
                                     'placeholder': _('Имя')
                                 }
                                 ))

    last_name = forms.CharField(label=_('Фамилия'), max_length=150,
                                widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'placeholder': _('Фамилия')
                                }))

    username_help_text = _("Обязательное поле. Не более 150 символов.\
                            Только буквы, цифры и символы @/./+/-/_.")
    password1 = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput(
                                attrs={
                                    'class': 'form-control',
                                    'placeholder': _('Пароль')
                                }
                                ))

    password2 = forms.CharField(label=_('Подтверждение пароля'),
                                widget=forms.PasswordInput(
                                attrs={
                                    'class': 'form-control',
                                    'placeholder': _('Подтверждение пароля')
                                }
                                ))
    password = forms.CharField(label='',
                               widget=forms.HiddenInput(), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'password1',
                  'password2',)
        exclude = ('password',)

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {
                "class": 'form-control',
                "placeholder": _('Имя пользователя'),
                "label": _('Имя пользователя'),
            }
        )
        self.fields['username'].validators = [MaxLengthValidator]
        self.fields['username'].label = _('Имя пользователя')

        self.fields['password1'].widget.attrs.update(
            {
                "class": 'form-control',
                "placeholder": _('Пароль'),
                "label": _('Пароль'),
                "min_size": 3,
            }
        )
        self.fields['password1'].label = _('Пароль')
        self.fields['password1'].help_text =\
            f'{_("Ваш пароль должен содержать как минимум 3 символа.")}'

        self.fields['password2'].widget.attrs.update(
            {
                "class": 'form-control',
                "placeholder": _('Подтверждение пароля'),
                "label": _('Пароль'),
            }
        )
        self.fields['password2'].label = _('Подтверждение пароля')
        self.fields['password2'].help_text =\
            _("Для подтверждения введите, пожалуйста, пароль ещё раз.")

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError(_('Введенные пароли не совпадают.'))
        if len(password2) < 3:
            raise ValidationError(_('Введённый пароль слишком короткий.\
             Он должен содержать как минимум 3 символа.'))
