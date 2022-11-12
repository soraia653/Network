from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):

    # fields of post
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=False, max_length=125)
    creation_date = models.DateTimeField(auto_now_add=True)
    num_likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "user": self.user.username,
            "post": self.text,
            "date": self.creation_date.strftime("%b %d %Y, %I:%M %p"),
            "num_likes": self.num_likes
        }

