from django.urls import path

from . import views

urlpatterns = [
    path("", views.TasksIndexView.as_view(), name="tasks"),
    path("create/", views.CreateTasksView.as_view(), name="create_task"),
    path(
        "<int:id>/update/", views.UpdateTasksView.as_view(), name="update_task"
    ),
    path(
        "<int:id>/delete/", views.DeleteTasksView.as_view(), name="delete_task"
    ),
    path("<int:id>/", views.TasksPageView.as_view(), name="page_task"),
]
