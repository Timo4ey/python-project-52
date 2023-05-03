from django.contrib import admin
from django.contrib.auth.models import Group, User
from task_manager.users.models import Profile


@admin.register(Profile)
class ProfilesAdmin(admin.ModelAdmin):
    list_display = ('username', 'timestamp')


admin.site.unregister(Group)


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username']


admin.site.unregister(User)
