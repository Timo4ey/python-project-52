# from django.contrib.auth.models import AbstractUser
#
#
# class User(AbstractUser):
#
#     def full_name(self):
#         return self.get_full_name()
#
#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'


from django.contrib.auth.models import User


def get_full_name(self):
    return f"{self.first_name} {self.last_name}"


User.add_to_class("__str__", get_full_name)
