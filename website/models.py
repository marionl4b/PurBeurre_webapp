from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()


class Product(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    API_link = models.URLField()
    photo = models.URLField()
    nutriscore = models.CharField(max_length=1)
    nutrient_100g = models.TextField(null=True)
    categories = models.ManyToManyField(Category)
