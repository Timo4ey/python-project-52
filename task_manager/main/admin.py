from django.contrib import admin
from django.contrib.auth.models import Group, User
from task_manager.users.models import Profile
from task_manager.tags.models import Tags
from task_manager.task_status.models import TaskStatus
from task_manager.tasks.models import Tasks


@admin.register(Profile)
class ProfilesAdmin(admin.ModelAdmin):
    list_display = ('username', 'timestamp')


admin.site.unregister(Group)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']


@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ['creator', 'name', 'description',
                    'status', 'performer']


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username']


# admin.site.unregister(User)
