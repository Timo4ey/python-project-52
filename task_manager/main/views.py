from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from task_manager.main.forms import UserLogingForm


class IndexViews(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class UserLoginView(View):
    # authenticate  login, logout
    def get(self, request, *args, **kwargs):
        form = UserLogingForm(auto_id="id_for_%s", label_suffix="")
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        t1 = _('Пожалуйста, введите правильные имя пользователя и пароль. ')
        t2 = _('Оба поля могут быть чувствительны к регистру.')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,
                            username=username,
                            password=password)
        if user is not None:
            login(request, user)
            messages.success(request, _('Вы залогинены'))
            return redirect('main')
        messages.add_message(request, messages.ERROR,
                             message=f'{t1}{t2}')
        form = UserLogingForm(request.POST, instance=User)
        return render(request, 'login.html', {'form': form})


class UserLogOutView(View):

    def get(self, request, *args, **kwarg):
        logout(request)
        messages.info(request, _('Вы разлогинены'))
        return redirect('main')


class IndexUser(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, 'users.html', {'users': users})
