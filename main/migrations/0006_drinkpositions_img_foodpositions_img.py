# Generated by Django 5.0 on 2023-12-24 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_restaurant_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='drinkpositions',
            name='img',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='foodpositions',
            name='img',
            field=models.TextField(default='1'),
            preserve_default=False,
        ),
    ]