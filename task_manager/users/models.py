from django.db import models
from django.utils.translation import gettext_lazy as _
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
    # def create_profile(self):


# Create Profile With New User Signs Up

# class User(models.Model):
#
#     first_name = models.CharField(null=False, max_length=150)
#     second_name = models.CharField(null=False, max_length=150)
#     username = models.CharField(null=False, max_length=150)
#     password = models.CharField(null=False, max_length=150)
#     created_at = models.DateTimeField(auto_now_add=True)
