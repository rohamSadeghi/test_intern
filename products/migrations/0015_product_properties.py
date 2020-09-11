# Generated by Django 2.2.14 on 2020-09-11 07:13

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20200911_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='properties',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
