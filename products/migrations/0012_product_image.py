# Generated by Django 2.2.14 on 2020-09-04 06:23

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20200904_0532'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to=products.models.product_images_path),
        ),
    ]
