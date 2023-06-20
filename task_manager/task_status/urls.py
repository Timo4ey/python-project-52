from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexViews.as_view(), name="statuses"),
    path("create/", views.StatusCreateView.as_view(), name="create_status"),
    path(
        "<int:id>/update/",
        views.StatusUpdateView.as_view(),
        name="update_status",
    ),
    path(
        "<int:id>/delete/",
        views.StatusDeleteView.as_view(),
        name="delete_status",
    ),
]
