# Generated by Django 3.1.5 on 2021-01-14 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210114_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aroma',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='feel',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='skin',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='texture',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
