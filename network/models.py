from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    Owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poster')
    Content = models.TextField(max_length=160)
    Timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" @{self.Owner} posted {self.destination} at {self.Timestamp}"

    def not_empty(self):
        return len(self.Content) > 0