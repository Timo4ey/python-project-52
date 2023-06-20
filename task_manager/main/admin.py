from django.contrib import admin
from django.contrib.auth.models import Group, User

from task_manager.labels.models import Label
from task_manager.task_status.models import TaskStatus
from task_manager.tasks.models import Tasks

admin.site.unregister(Group)


@admin.register(Label)
class TagsAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]


@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ["creator", "name", "description", "status", "executor"]


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
