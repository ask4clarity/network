from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    Owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poster')
    Content = models.TextField(max_length=160)
    Timestamp = models.DateTimeField(auto_now_add=True)
    Likes = models.ManyToManyField(User, related_name="liker", null=True)

    def __str__(self):
        return f" @{self.Owner} posted {self.Content} at {self.Timestamp}"

    def not_empty(self):
        return len(self.Content) > 0

    def total_likes(self):
        return self.Likes.count()    

    def serialize(self):
        return {
            "id": self.id,
            "owner": self.Owner.username,
            "content": self.Content,
            "timestamp": self.Timestamp,
            "likes": self.total_likes()
        }

class Follow(models.Model):
    Owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    Target = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='followed')

    def __str__(self):
        return f" @{self.Owner} follows @{self.Target}"

    def not_same(self):
        return self.Owner != self.Target

