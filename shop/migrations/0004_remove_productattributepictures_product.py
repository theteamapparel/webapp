# Generated by Django 4.0.1 on 2023-03-08 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_rename_product_description_product_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productattributepictures',
            name='product',
        ),
    ]
