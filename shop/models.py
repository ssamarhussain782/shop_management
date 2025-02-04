from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from uuid import uuid4

class Shop(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_shops'
    )
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=1024, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name='categories'
    )
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        unique_together = ('name', 'shop')


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    mrp = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], null=True, blank=True
    )
    inventory = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)]
    )
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name='products'
    )
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        unique_together = ('name', 'shop')


class Sale(models.Model):
    receipt_number = models.CharField(max_length=50, unique=True, editable=False)
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name='sales'
    )
    sale_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = str(uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale #{self.receipt_number}"

    class Meta:
        ordering = ['-sale_date']


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def save(self, *args, **kwargs):
        is_new = self._state.adding


        if not is_new:
            original = SaleItem.objects.get(pk=self.pk)
            inventory_adjustment = self.quantity - original.quantity
        else:
            inventory_adjustment = self.quantity

        if self.product.inventory < inventory_adjustment:
            raise ValueError(f"Not enough inventory for product {self.product.name}.")

        # Adjust the product's inventory
        self.product.inventory -= inventory_adjustment
        self.product.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.product.inventory += self.quantity
        self.product.save()
        super().delete(*args, **kwargs)

    @property
    def unit_price(self):
        return self.product.price

    def __str__(self):
        return f"{self.product.name} - {self.quantity} x {self.unit_price}"

    class Meta:
        unique_together = ('sale', 'product')
