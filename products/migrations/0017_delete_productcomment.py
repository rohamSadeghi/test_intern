# Generated by Django 2.2.14 on 2020-09-17 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_productcomment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductComment',
        ),
    ]
