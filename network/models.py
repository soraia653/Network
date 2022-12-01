from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):

    # fields of post
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=False, max_length=125)
    creation_date = models.DateTimeField(auto_now_add=True)
    num_likes = models.ManyToManyField(User, related_name='posts_like')

    # function will return number of likes of post
    def count_likes(self):
        return self.num_likes.count()

    def serialize(self):
        return {
            "username": self.user.username,
            "post": self.text,
            "date": self.creation_date.strftime("%b %d %Y, %I:%M %p"),
            "num_likes": self.num_likes
        }

class Following(models.Model):
    user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    started_following = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # can't follow same user twice
            models.UniqueConstraint(fields=['user', 'following_user'], name='no_follow_twice'),

            # can't follow themselves (~ is used to negate something)
            models.CheckConstraint(name="prevent_self_follow", 
            check = ~models.Q(following_user = models.F('user')))
        ]
    
    def __str__(self):
        return f"{self.user} follows {self.following_user}"