# Generated by Django 4.0.10 on 2023-02-24 12:36

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_dish_image_alter_dish_title_alter_menu_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=core.models.dish_image_file_path),
        ),
    ]
