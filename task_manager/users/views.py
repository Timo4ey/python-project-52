from django.shortcuts import render, reverse, redirect, HttpResponsePermanentRedirect
from django.views import View
from task_manager.users.forms import UserRegistrationForm, UserLogingForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.
class UserFormCreateView(View):
    def get(self, request, *args, **kwargs):
        form = UserRegistrationForm()  # auto_id="id_for_%s", label_suffix=""
        return render(request, 'profiles/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            return HttpResponsePermanentRedirect(reverse('login'))
        return render(request, 'profiles/create.html', {'form': form})


class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        form = UserLogingForm(auto_id="id_for_%s", label_suffix="")
        return render(request, 'profiles/login.html', {'form': form})

    def post(self, request, *args, **kwarg):
        ...


class IndexUser(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'profiles/index.html')
