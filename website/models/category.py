from django.db import models


class Category(models.Model):
    """Models for categories of OFF products"""
    name = models.CharField(max_length=100, unique=True)
    desc = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'website'
