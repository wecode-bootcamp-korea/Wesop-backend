# Generated by Django 3.1.5 on 2021-01-14 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(default='KO-KR', max_length=45),
        ),
    ]