"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# import task_manager.views as views
# from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('task_manager.main.urls'), name='main'),
    path('users/', include('task_manager.users.urls'), name='users'),
    path('statuses/', include('task_manager.task_status.urls'), name='statuses'),
    path('tags/', include('task_manager.tags.urls'), name='tags'),
    path('tasks/', include('task_manager.tasks.urls'), name='tasks'),

    # path('i18n/', include('django.conf.urls.i18n')),
]

# urlpatterns += i18n_patterns(
#     path('', views.IndexViews.as_view(), name='index'),
# )
