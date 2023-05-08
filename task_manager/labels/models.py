from django.db import models


class Tags(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tasks = models.ManyToManyField("self")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
