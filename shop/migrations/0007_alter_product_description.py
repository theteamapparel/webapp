# Generated by Django 4.0.1 on 2023-03-09 05:28

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_productreview_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=tinymce.models.HTMLField(blank=True, default=''),
        ),
    ]
