# Generated by Django 2.1.7 on 2019-03-25 10:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0005_auto_20190325_1047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('desc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('desc', models.TextField()),
                ('API_link', models.URLField()),
                ('photo', models.URLField()),
                ('nutriscore', models.CharField(max_length=1)),
                ('nutrient_100g', models.TextField(null=True)),
                ('categories', models.ManyToManyField(to='website.Category')),
                ('favorites', models.ManyToManyField(related_name='Favorite', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
