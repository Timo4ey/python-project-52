from django.contrib import messages
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views import View
from .models import TaskStatus
from django.utils.translation import gettext_lazy as _
from .forms import FormTaskStatus
from ..tasks.models import Tasks


# Create your views here.


class IndexViews(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            statuses = TaskStatus.objects.all()
            return render(request, 'status/index.html', {'statuses': statuses})
        messages.error(request, _('Вы не авторизованы! Пожалуйста, выполните вход.'))
        return redirect(reverse('login'))


class StatusCreateView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = FormTaskStatus()
            return render(request, 'status/create.html', {'form': form})
        messages.error(request, _('Вы не авторизованы! Пожалуйста, выполните вход.'))
        return redirect(reverse('login'))

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = FormTaskStatus(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, message=_('Статус успешно создан'))
                return redirect('statuses')
            return render(request, 'status/update.html', {'form': form})
        messages.error(request, _('Вы не авторизованы! Пожалуйста, выполните вход.'))
        return redirect(reverse('login'))


class StatusUpdateView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(request.user.id)
            instance = TaskStatus.objects.get(id=kwargs.get('id'))
            form = FormTaskStatus(instance=instance)
            return render(request, 'status/update.html', {'form': form,
                                                          'id': kwargs.get('id')})
        messages.error(request, _('Вы не авторизованы! Пожалуйста, выполните вход.'))
        return redirect(reverse('login'))

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        if request.user.is_authenticated:
            instance = TaskStatus.objects.get(id=status_id)
            form = FormTaskStatus(request.POST, instance=instance)
            new_name = request.POST.get('name')

            if instance.name != new_name and TaskStatus.objects.filter(name=new_name):
                return render(request, 'status/update.html', {'form': form, 'id': status_id})
            if form.is_valid():
                form.save()
                messages.success(request, message=_('Статус успешно изменён'))
                return redirect('statuses')
        messages.error(request, _('Вы не авторизованы! Пожалуйста, выполните вход.'))
        return redirect(reverse('login'))


class StatusDeleteView(View):
    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        if request.user.is_authenticated:
            name = get_object_or_404(TaskStatus, id=status_id)
            return render(request, 'status/delete.html', {
                'name': name.name,
                'status_id': status_id
            }
                          )

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            status_id = kwargs.get('id')
            status = get_object_or_404(TaskStatus, id=status_id)
            tasks = Tasks.objects.filter(status=status).exists()
            if tasks:
                messages.error(request, _('Невозможно удалить метку, потому что она используется'))
                return redirect('statuses')
            status.delete()
        messages.success(request, message=_('Статус успешно удалён'))
        return redirect('statuses')
