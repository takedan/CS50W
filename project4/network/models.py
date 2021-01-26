from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuarios")
    text = models.TextField(max_length=280)
    likes = models.IntegerField()
    datecreation = models.DateField(auto_now=True)    

    def __str__(self):
        return f"{self.user} POST N {self.id}"

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuarios_follow")
    list = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.user}"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuarios_comment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="posts")
    text = models.TextField(max_length=280)
    likes = models.IntegerField()
    datecreation = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user}" 