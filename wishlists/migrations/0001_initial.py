# Generated by Django 4.2.2 on 2023-06-26 01:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cafes', '0004_cafe_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('experiences', '0002_experience_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='만든날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='변경날짜')),
                ('name', models.CharField(max_length=30)),
                ('cafes', models.ManyToManyField(to='cafes.cafe')),
                ('experiences', models.ManyToManyField(to='experiences.experience')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]