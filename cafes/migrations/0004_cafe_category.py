# Generated by Django 4.2.2 on 2023-06-23 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('cafes', '0003_alter_facility_options_alter_cafe_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cafe',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='categories.category'),
        ),
    ]
