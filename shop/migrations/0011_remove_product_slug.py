# Generated by Django 5.1.4 on 2025-01-20 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_remove_saleitem_unit_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]
