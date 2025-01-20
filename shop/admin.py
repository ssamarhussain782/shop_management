from django.contrib import admin
from .models import Shop, ProductCategory, Product, Sale, SaleItem


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'description', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'owner__username', 'owner__email')


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'description')
    list_filter = ('shop',)
    search_fields = ('name', 'shop__name')
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'mrp', 'inventory', 'category', 'shop', 'added_at', 'updated_at')
    list_filter = ('shop', 'category', 'added_at', 'updated_at')
    search_fields = ('name', 'category__name', 'shop__name')
    ordering = ('name',)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'shop__name', 'amount', 'sale_date')
    list_filter = ['sale_date']
    search_fields = ['receipt_number']
    date_hierarchy = 'sale_date'

    # Add a dynamic property for the total sale amount
    def amount(self, obj):
        return sum(item.quantity * item.unit_price for item in obj.items.all())
    amount.short_description = 'Total Amount'


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'quantity', 'get_unit_price')
    list_filter = ['product__category']
    search_fields = ('sale__receipt_number', 'product__name')

    def get_unit_price(self, obj):
        return obj.unit_price
    get_unit_price.short_description = 'Unit Price'


