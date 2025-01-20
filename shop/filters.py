import django_filters
from django_filters import rest_framework as filters
from .models import Product, Sale, SaleItem
from datetime import datetime

class ProductFilter(filters.FilterSet):
    # category = filters.ModelChoiceFilter(queryset=ProductCategory.objects.all(), field_name='category')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_inventory = filters.NumberFilter(field_name='inventory', lookup_expr='gte')
    max_inventory = filters.NumberFilter(field_name='inventory', lookup_expr='lte')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    added_at_start = filters.DateTimeFilter(field_name='added_at', lookup_expr='gte')
    added_at_end = filters.DateTimeFilter(field_name='added_at', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price', 'min_inventory', 'max_inventory', 'name', 'added_at_start', 'added_at_end']



class SaleFilter(django_filters.FilterSet):
    # Filtering by sale date range
    start_date = filters.DateTimeFilter(field_name="sale_date", lookup_expr='gte', label="Start Date")
    end_date = filters.DateTimeFilter(field_name="sale_date", lookup_expr='lte', label="End Date")

    # Filtering by total sale amount range
    min_amount = filters.NumberFilter(field_name='total_amount', lookup_expr='gte', label="Min Amount")
    max_amount = filters.NumberFilter(field_name='total_amount', lookup_expr='lte', label="Max Amount")

    # Optional: If you need to filter by specific sales person
    salesperson = filters.NumberFilter(field_name='salesperson__id', lookup_expr='exact', label="Salesperson ID")

    class Meta:
        model = Sale
        fields = ['start_date', 'end_date', 'min_amount', 'max_amount', 'salesperson']

class SaleItemFilter(django_filters.FilterSet):
    sale = filters.NumberFilter(field_name='sale', lookup_expr='exact', label='sale_id')  # Support 'sale_id'
    product = filters.NumberFilter(field_name='product', lookup_expr='exact')

    class Meta:
        model = SaleItem
        fields = ['sale', 'product']
