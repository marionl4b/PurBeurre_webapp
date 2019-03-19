from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    API_link = models.URLField()
    photo = models.URLField()
    nutriscore = models.CharField(max_length=1)
    nutrient_100g = models.TextField(null=True)
    categories = models.ManyToManyField(Category)
    favorites = models.ManyToManyField(User, related_name="Favorite")

    def __str__(self):
        return self.name
