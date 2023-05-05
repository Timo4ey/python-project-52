from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from task_manager.tasks.models import Tasks
from task_manager.users.forms import SignUpForm, UpdateForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


# Create your views here.
class IndexUser(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, 'users/users.html', {'users': users})


class UserFormCreateView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'users/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            messages.success(request, message=_('Пользователь успешно зарегистрирован'))
            return redirect('login')
        return render(request, 'users/create.html', {'form': form}, status=400)


class UserUpdateView(View):

    def get(self, request,  *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('login')

        if user.id == kwargs.get('id'):
            current_user = User.objects.get(id=user.id)
            form = UpdateForm(instance=current_user)
            return render(request, 'users/update.html', {'form': form})

        messages.error(request, _('У вас нет прав для изменения другого пользователя.'))
        return redirect('users')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            current_user = User.objects.get(id=user.id)
            form = UpdateForm(data=request.POST or None, instance=current_user)
            if form.is_valid():
                form.save()
                messages.success(request, _('Пользователь успешно изменён'))
                return redirect('users')
        form = UpdateForm(request.POST)
        return render(request, 'users/update.html', {'form': form}, status=400)


class UserDeleteView(View):
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        task = Tasks.objects.filter(creator_id=user_id)
        if request.user.is_authenticated and user_id == kwargs.get('id'):
            if not task:
                first_name = request.user.first_name
                last_name = request.user.last_name
                return render(request, 'users/delete.html', {'full_name': f'{first_name} {last_name}'})
            messages.error(request, _('Невозможно удалить пользователя, потому что он используется'))
            return redirect('users')
        if not request.user.is_authenticated:
            messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('login')
        messages.error(request, _('У вас нет прав для изменения другого пользователя.'))
        return redirect('users')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.id == kwargs.get('id'):
            user = User.objects.get(id=request.user.id)
            user.delete()
        return redirect('main')
