from django.shortcuts import render
from django.views.generic.base import View


class IndexViews(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")
