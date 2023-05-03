from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from task_manager.users.models import Profile# unregister groups


@admin.register(Profile)
class ProfilesAdmin(admin.ModelAdmin):
    list_display = ('username', 'timestamp')

admin.site.unregister(Group)


class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

#
#
# # Mix Profile info into User info
# class ProfileInline(admin.StackedInline):
#     model = Profile
# # extend User Model
#
#
class UserAdmin(admin.ModelAdmin):
    model = User
    # just display admin page
    fields = ['username']
    # inlines = [ProfileInline]
#
#
# # unregister user
admin.site.unregister(User)
#
# # register user
admin.site.register(User, CustomUserAdmin)
# admin.site.register(Profile)
