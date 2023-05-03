# from django.contrib import admin
from django.urls import path
import task_manager.main.views as views


urlpatterns = [
    path('', views.IndexViews.as_view(), name='main'),
    path('users/', views.IndexUser.as_view(), name='users'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogOutView.as_view(), name='logout'),
    path('create/', views.UserFormCreateView.as_view(), name='create'),
    path('users/<int:id>/update/', views.UserUpdateView.as_view(), name='update'),
]
