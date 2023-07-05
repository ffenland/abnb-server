# Generated by Django 4.2.2 on 2023-07-05 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='nickname',
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.URLField(blank=True, null=True),
        ),
    ]
