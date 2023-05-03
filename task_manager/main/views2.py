from django.shortcuts import render, reverse, redirect, HttpResponsePermanentRedirect
from django.utils.translation import gettext as _
from django.views.generic.base import View, TemplateView
from .forms import UserLogingForm, SignUpForm, UpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.


class IndexViews(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


# Create your views here.
class UserFormCreateView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()  # auto_id="id_for_%s", label_suffix=""
        return render(request, 'create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, message=_('Пользователь успешно зарегистрирован'))
            return HttpResponsePermanentRedirect(reverse('login'))
        return render(request, 'create.html', {'form': form})


class UserLoginView(View):
    # authenticate  login, logout
    def get(self, request, *args, **kwargs):
        form = UserLogingForm(auto_id="id_for_%s", label_suffix="")
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,
                            username=username,
                            password=password)
        if user is not None:
            login(request, user)
            messages.success(request, _('Вы залогинены'))
            return redirect('main')
        messages.add_message(request, messages.ERROR,
                             message=_('Пожалуйста, введите правильные имя пользователя и пароль. \
                             Оба поля могут быть чувствительны к регистру.'))
        form = UserLogingForm(request.POST, instance=User)
        return render(request, 'login.html', {'form': form})


# def update_user(request, *args, **kwargs):
#
#     if request.user.is_authenticated:
#         current_user = User.objects.get(id=request.user.id)
#         # Get Forms
#         user_form = UserRegistrationForm(request.POST or None, instance=current_user)
#         if user_form.is_valid():
#             user_form.save()
#             login(request, current_user)
#             messages.success(request, ("Your Profile Has Been Updated!"))
#             return redirect('users')
#         return render(request, "update.html", {'user_form':user_form})
#     else:
#         messages.success(request, ("You Must Be Logged In To View That Page..."))
#         return redirect('login')

class UserUpdateView(View):

    def get(self, request,  *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('login')

        if user.id == kwargs.get('id'):
            current_user = User.objects.get(id=user.id)
            form = UpdateForm(request.POST or None, instance=current_user)
            return render(request, 'update.html', {'form': form})

        messages.error(request, _('У вас нет прав для изменения другого пользователя.'))
        return redirect('users')

    def post(self, request, *args, **kwargs):
        print('!!!')
        if request.user.is_authenticated:
            user = request.user
            current_user = User.objects.get(id=user.id)
            form = UpdateForm(data=request.POST or None, instance=current_user)

            if form.is_valid():
                print('!!!')
                form.save()
                messages.success(request, _('Пользователь успешно изменён'))
                return redirect('users')
        form = UpdateForm(request.POST)
        return render(request, 'update.html', {'form': form})

class UserLogOutView(View):

    def get(self, request, *args, **kwarg):
        logout(request)
        messages.info(request, _('Вы разлогинены'))
        return redirect('main')


class IndexUser(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, 'users.html', {'users': users})
