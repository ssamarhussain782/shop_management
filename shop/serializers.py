from rest_framework import serializers
from .models import Shop, Product, ProductCategory, Sale, SaleItem
from django.conf import settings


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = super().create(validated_data)
        # Set the user's shop (example logic, adjust as per your requirements)
        user.shop = Shop.objects.get(name='Default Shop')  # Example logic
        user.save()
        return user


class ProductCategorySerializer(serializers.ModelSerializer):
    shop = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.none())  # Default to empty queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Restrict the shop queryset to the user's shops
        user = self.context['request'].user
        if user.is_authenticated:
            self.fields['shop'].queryset = Shop.objects.filter(owner=user)

    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Restrict the shop queryset to the user's shops
        user = self.context['request'].user
        if user.is_authenticated:
            self.fields['shop'].queryset = Shop.objects.filter(owner=user)

    class Meta:
        model = Product
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    receipt_number = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    # Filter the shops based on the logged-in user
    shop = serializers.PrimaryKeyRelatedField(
        queryset=Shop.objects.none()  # Default to empty queryset
    )

    def __init__(self, *args, **kwargs):
        request = kwargs['context']['request']
        super().__init__(*args, **kwargs)
        # Filter shops for the authenticated user
        if request and request.user.is_authenticated:
            self.fields['shop'].queryset = Shop.objects.filter(owner=request.user)

    class Meta:
        model = Sale
        fields = ['id', 'receipt_number', 'shop', 'sale_date']

class SaleItemSerializer(serializers.ModelSerializer):
    """SaleItem serializer to dynamically fetch product price and display receipt_number."""

    # Fetch the receipt number from the sale table
    receipt_number = serializers.ReadOnlyField(source='sale.receipt_number')
    # Fetch the product price dynamically (read-only)
    product_price = serializers.DecimalField(
        source='product.price', max_digits=10, decimal_places=2, read_only=True
    )

    sale = serializers.PrimaryKeyRelatedField(
        queryset=Sale.objects.none()  # Default to an empty queryset initially
    )
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.none()  # Default to an empty queryset initially
    )

    def __init__(self, *args, **kwargs):
        """Filter sales and products for the authenticated user's shop."""
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user_shop = Shop.objects.filter(owner=request.user)
            self.fields['sale'].queryset = Sale.objects.filter(shop__in=user_shop)
            self.fields['product'].queryset = Product.objects.filter(shop__in=user_shop)

    class Meta:
        model = SaleItem
        fields = ['id', 'sale', 'receipt_number', 'product', 'quantity', 'product_price']


class ProductSoldSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    total_quantity_sold = serializers.IntegerField()
    total_sales_value = serializers.DecimalField(max_digits=10, decimal_places=2)