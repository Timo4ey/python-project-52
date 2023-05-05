from django.contrib import messages
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views import View
from .models import Tags
from django.utils.translation import gettext_lazy as _
from .forms import FormTag
# Create your views here.


class IndexViews(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            tags = Tags.objects.all()
            return render(request, 'tag/index.html', {'tags': tags})
        messages.error(request, _('Вы не авторизованы! Пожалуйста, выполните вход.'))
        return redirect(reverse('login'))


class TagCreateView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = FormTag()
            return render(request, 'tag/create.html', {'form': form})
        messages.error(request, _('Вы не авторизованы! Пожалуйста, выполните вход.'))
        return redirect(reverse('login'))

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = FormTag(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, message=_('Тег успешно создан'))
                return redirect('tags')
            return render(request, 'tag/update.html', {'form': form})
        messages.error(request, _('Вы не авторизованы! Пожалуйста, выполните вход.'))
        return redirect(reverse('login'))


class TagUpdateView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(request.user.id)
            instance = Tags.objects.get(id=kwargs.get('id'))
            form = FormTag(instance=instance)
            return render(request, 'tag/update.html', {'form': form,
                                                       'id': kwargs.get('id')})
        messages.error(request, _('Вы не авторизованы! Пожалуйста, выполните вход.'))
        return redirect(reverse('login'))

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        if request.user.is_authenticated:
            instance = Tags.objects.get(id=status_id)
            form = FormTag(request.POST, instance=instance)
            new_name = request.POST.get('name')

            if instance.name != new_name and Tags.objects.filter(name=new_name):
                return render(request, 'tag/update.html', {'form': form, 'id': status_id})
            if form.is_valid():
                form.save()
                messages.success(request, message=_('Тег успешно изменён'))
                return redirect('tags')
        messages.error(request, _('Вы не авторизованы! Пожалуйста, выполните вход.'))
        return redirect(reverse('login'))


class TagDeleteView(View):
    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        if request.user.is_authenticated:
            name = get_object_or_404(Tags, id=status_id)
            return render(request, 'tag/delete.html', {
                'name': name.name,
                'status_id': status_id
            }
                          )

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            status_id = kwargs.get('id')
            status = get_object_or_404(Tags, id=status_id)
            status.delete()
        messages.success(request, message=_('Тег успешно удалён'))
        return redirect('tags')
