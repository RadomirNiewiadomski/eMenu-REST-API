# Generated by Django 4.0.10 on 2023-02-23 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_dish_created_date_alter_menu_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='created_date',
            field=models.DateField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='modified_date',
            field=models.DateField(auto_now=True, verbose_name='Modified'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='created_date',
            field=models.DateField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='modified_date',
            field=models.DateField(auto_now=True, verbose_name='Modified'),
        ),
    ]