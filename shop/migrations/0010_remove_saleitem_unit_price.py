# Generated by Django 5.1.4 on 2025-01-20 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_product_mrp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saleitem',
            name='unit_price',
        ),
    ]
