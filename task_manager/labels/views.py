from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils.translation import gettext_lazy as _
from django.views import View

from ..tasks.models import Tasks
from .forms import FormLabel
from .models import Label

# Create your views here.


class IndexViews(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            labels = Label.objects.all()
            return render(request, "label/index.html", {"labels": labels})
        messages.error(
            request, _("Вы не авторизованы! Пожалуйста, выполните вход.")
        )
        return redirect(reverse("login"))


class LabelCreateView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = FormLabel()
            return render(request, "label/create.html", {"form": form})
        messages.error(
            request, _("Вы не авторизованы! Пожалуйста, выполните вход.")
        )
        return redirect(reverse("login"))

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = FormLabel(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, message=_("Метка успешно создана"))
                return redirect("labels")
            return render(request, "label/create.html", {"form": form})
        messages.error(
            request, _("Вы не авторизованы! Пожалуйста, выполните вход.")
        )
        return redirect(reverse("login"))


class LabelUpdateView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(request.user.id)
            instance = Label.objects.get(id=kwargs.get("id"))
            form = FormLabel(instance=instance)
            return render(
                request,
                "label/update.html",
                {"form": form, "id": kwargs.get("id")},
            )
        messages.error(
            request, _("Вы не авторизованы! Пожалуйста, выполните вход.")
        )
        return redirect(reverse("login"))

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get("id")
        if request.user.is_authenticated:
            instance = Label.objects.get(id=status_id)
            form = FormLabel(request.POST, instance=instance)
            new_name = request.POST.get("name")

            if instance.name != new_name and Label.objects.filter(
                name=new_name
            ):
                return render(
                    request,
                    "label/update.html",
                    {"form": form, "id": status_id},
                )
            if form.is_valid() or instance.name == new_name:
                if form.is_valid():
                    form.save()
                messages.success(request, message=_("Метка успешно изменена"))
                return redirect("labels")
        messages.error(
            request,
            _(
                "Вы не авторизованы! Пожалуйста, выполните вход."
            ),
        )
        return redirect(reverse("login"))


class LabelDeleteView(View):
    def get(self, request, *args, **kwargs):
        label_id = kwargs.get("id")
        if request.user.is_authenticated:
            name = get_object_or_404(Label, id=label_id)
            return render(
                request,
                "label/delete.html",
                {"name": name.name, "label_id": label_id},
            )

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            label_id = kwargs.get("id")
            label = get_object_or_404(Label, id=label_id)
            tasks = Tasks.objects.filter(labels=label).exists()
            if tasks:
                messages.error(
                    request,
                    _(
                        "Невозможно удалить метку, потому что она используется"
                    ),
                )
                return redirect("labels")
            label.delete()
        messages.success(request, message=_("Метка успешно удалена"))
        return redirect("labels")
