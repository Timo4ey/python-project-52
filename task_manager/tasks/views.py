from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import CreateTaskForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Tasks
from .filters import TaskFilter


class TasksIndexView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            tasks = Tasks.objects.all()
            tasks_filter = TaskFilter(request.GET, request=request, queryset=tasks)
            return render(request, 'tasks/index.html', {
                'tasks': tasks,
                'filter': tasks_filter,
            })
        return redirect('login')


class TasksPageView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            task_id = kwargs.get('id')
            task = get_object_or_404(Tasks, id=task_id)
            return render(request, 'tasks/task_page.html', {'task': task, 'id': task_id})
        return redirect('login')


class CreateTasksView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = CreateTaskForm(request.POST or None)   # {'creator': request.user}
            return render(request, 'tasks/create.html', {'form': form})
        messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
        return redirect('login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = CreateTaskForm(request.POST or None)
            if form.is_valid():
                label = request.POST.getlist('labels')
                task = form.save(commit=False)
                task.creator = request.user

                task.save()
                if label:
                    [task.labels.add(i) for i in label]
                    task.save()
                else:
                    task.save()
                messages.success(request, _('Задача успешно создана'))
                return redirect('tasks')
            return render(request, 'tasks/create.html', {'form': form}, status=400)


class UpdateTasksView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            task_id = kwargs.get('id')
            instance = Tasks.objects.get(id=task_id)
            form = CreateTaskForm(request.POST or None, instance=instance)
            return render(request, 'tasks/update.html', {'form': form, 'id': task_id})
        messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
        return redirect('login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            task_id = kwargs.get('id')
            instance = Tasks.objects.get(id=task_id)
            form = CreateTaskForm(request.POST or None, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, _('Задача успешно изменена'))
                return redirect('tasks')
            return render(request, 'tasks/update.html', {'form': form, 'id': task_id}, status=400)


class DeleteTasksView(View):
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            user_id = request.user.id
            task_id = kwargs.get('id')
            task = Tasks.objects.get(id=task_id)
            if task.creator_id == user_id:
                tasks = Tasks.objects.get(id=task_id)
                name = tasks.name
                return render(request, 'tasks/delete.html', {'id': task_id, 'name': name})
            messages.error(request, _("Задачу может удалить только её автор"))
            return redirect('tasks')
        messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
        return redirect('login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            task_id = kwargs.get('id')
            task = Tasks.objects.get(id=task_id)
            if task.creator_id == request.user.id:
                task.delete()
                messages.success(request, _('Задача успешно удалена'))
                return redirect('tasks')
            messages.error(request, _("Задачу может удалить только её автор"))
            return redirect('tasks')
        messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
        return redirect('login')
