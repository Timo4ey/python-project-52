from django.db import models


class TaskStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tasks = models.ManyToManyField("self")
    created_at = models.DateTimeField(auto_now_add=True)
