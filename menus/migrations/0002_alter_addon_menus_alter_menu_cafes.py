# Generated by Django 4.2.2 on 2023-07-06 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0004_cafe_category'),
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addon',
            name='menus',
            field=models.ManyToManyField(to='menus.menu'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='cafes',
            field=models.ManyToManyField(to='cafes.cafe'),
        ),
    ]
