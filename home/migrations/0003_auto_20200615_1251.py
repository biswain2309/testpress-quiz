# Generated by Django 2.2.9 on 2020-06-15 12:51

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20200615_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='ans',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), blank=True, null=True, size=4),
        ),
    ]
