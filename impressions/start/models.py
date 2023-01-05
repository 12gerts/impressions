from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=255, null=True, blank=True)

    def get_name_and_avatar(self):
        name = f'{self.user.first_name} {self.user.last_name}'
        return {"name": name, "avatar": self.avatar}

    def __str__(self):
        return f"User: {self.user.username}"
