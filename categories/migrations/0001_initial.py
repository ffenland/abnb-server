# Generated by Django 4.2.2 on 2023-06-23 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='만든날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='변경날짜')),
                ('name', models.CharField(max_length=30)),
                ('kind', models.CharField(choices=[('cafes', 'For Cafes'), ('experiencies', 'For Experiencies')], max_length=12)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
