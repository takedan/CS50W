from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm

class User(AbstractUser):
    pass

class ItemCategory(models.Model):
    CategoryID = models.AutoField(primary_key=True)
    Category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.Category}"

class CreateList(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuarios")
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.IntegerField()
    imageurl = models.URLField()
    datecreation = models.DateField(auto_now=True)
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, related_name="categorias")

    def __str__(self):
        return f"{self.title}"

class BidItem(models.Model):
    item = models.ForeignKey(CreateList, on_delete=models.CASCADE)
    bid = models.IntegerField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.usuario} BID {self.item}: ${self.bid}"