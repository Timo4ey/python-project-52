from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from task_manager.labels.models import Label
from task_manager.task_status.models import TaskStatus


class Tasks(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT,
                                related_name='creator_tasks',)
    name = models.CharField(max_length=150, null=False,  unique=True)
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE,
                               related_name='chosen_status')
    performer = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='chosen_performer',
                                  null=True,
                                  blank=True)
    labels = models.ManyToManyField(Label, related_name='chosen_tag', symmetrical=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def create_task(self, sender, instance, created, **kwargs):
        if created:
            users_task = self.__class__(user=instance)
            users_task.save()
            post_save.connect(self.create_task, sender=User)
