# Generated by Django 3.1.5 on 2021-01-20 02:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210120_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='mediatype',
        ),
    ]