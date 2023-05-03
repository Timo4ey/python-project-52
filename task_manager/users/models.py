from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(User, max_length=150)
    tasks = models.ManyToManyField("self",
                                   related_name="tasked_by",
                                   symmetrical=False,
                                   blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username}'

    def __create_profile(self, sender, instance, created, **kwargs):
        if created:
            user_profile = self.__class__(user=instance)
            user_profile.save()
            post_save.connect(self.__create_profile, sender=User)
