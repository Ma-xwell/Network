from django.contrib.auth.models import AbstractUser
from django.db import models


def get_default_following():
    return User.objects.none()


class User(AbstractUser):
    number_of_followers = models.PositiveIntegerField(default=0)
    number_of_following = models.PositiveIntegerField(default=0)
    followers = models.ManyToManyField('self', symmetrical=False, related_name="user_followers")
    following = models.ManyToManyField('self', symmetrical=False, related_name="user_following")
    liked_posts = models.ManyToManyField('Post', symmetrical=False, related_name="user_liked")


class Post(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    text = models.CharField(max_length=250)
    date = models.DateTimeField()
    likes = models.PositiveIntegerField(default=0)
    