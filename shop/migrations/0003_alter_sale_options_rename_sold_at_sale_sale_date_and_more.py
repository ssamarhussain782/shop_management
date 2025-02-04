# Generated by Django 5.1.4 on 2024-12-25 20:55

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_product_options_alter_sale_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sale',
            options={'ordering': ['-sale_date']},
        ),
        migrations.RenameField(
            model_name='sale',
            old_name='sold_at',
            new_name='sale_date',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='customer_name',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='product',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='total_price',
        ),
        migrations.AddField(
            model_name='sale',
            name='receipt_number',
            field=models.CharField(default='+', editable=False, max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sale',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10),
        ),
        migrations.AlterField(
            model_name='sale',
            name='salesperson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.salesperson'),
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.product')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shop.sale')),
            ],
            options={
                'unique_together': {('sale', 'product')},
            },
        ),
    ]
