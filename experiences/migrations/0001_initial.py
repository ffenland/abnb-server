# Generated by Django 4.2.2 on 2023-06-23 03:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='만든날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='변경날짜')),
                ('name', models.CharField(max_length=50)),
                ('details', models.CharField(blank=True, max_length=250, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='만든날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='변경날짜')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=80)),
                ('price', models.PositiveIntegerField()),
                ('start_at', models.TimeField()),
                ('end_at', models.TimeField()),
                ('description', models.TextField()),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('perks', models.ManyToManyField(to='experiences.perk')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
