# Generated by Django 5.1.4 on 2025-01-19 09:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_remove_sale_total_amount_remove_saleitem_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='shop',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='shop.shop'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sale',
            name='salesperson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='shop.salesperson'),
        ),
    ]
