# Generated by Django 5.1.4 on 2025-01-20 07:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_remove_sale_salesperson_delete_salesperson'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='mrp',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
    ]
