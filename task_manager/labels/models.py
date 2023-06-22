from django.db import models
from django.urls import reverse_lazy


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tasks = models.ManyToManyField("self")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url_upd(self):
        return reverse_lazy("update_label", kwargs={"id": self.id})

    def get_absolute_url_delete(self):
        return reverse_lazy("delete_label", kwargs={"id": self.id})
