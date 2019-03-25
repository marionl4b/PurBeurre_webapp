from django.db import models


class Category(models.Model):
    """Models for categories of OFF products"""
    name = models.CharField(max_length=100, unique=True, verbose_name="nom")
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'website'
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
