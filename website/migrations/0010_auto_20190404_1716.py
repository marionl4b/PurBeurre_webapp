# Generated by Django 2.2 on 2019-04-04 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20190404_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='nutrient_100g',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='nutriments(100g)'),
        ),
    ]
