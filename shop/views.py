from rest_framework import viewsets
from rest_framework.response import Response
from .models import Shop, Product, ProductCategory, Sale, SaleItem
from .serializers import ShopSerializer, ProductCategorySerializer, ProductSerializer, \
    SaleSerializer, SaleItemSerializer, ProductSoldSerializer
from .filters import ProductFilter, SaleFilter, SaleItemFilter
from rest_framework.permissions import IsAuthenticated  # Assuming permission for authentication
from .permissions import IsShopOwner  # Use IsShopOwner instead of CustomPermission
from django.db.models import F, Sum, Subquery, OuterRef, ExpressionWrapper, DecimalField
from django.shortcuts import get_object_or_404


# View for Shop
class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated, IsShopOwner]

    def get_queryset(self):
        return Shop.objects.filter(owner=self.request.user)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Product Categories.
    Only returns categories associated with the logged-in user's shop(s).
    """
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated, IsShopOwner]
    pagination_class = None

    def get_queryset(self):
        """
        Restrict queryset to categories belonging to the authenticated user's shop(s).
        """
        user = self.request.user
        if user.is_authenticated:
            return ProductCategory.objects.filter(shop__owner=user)
        return ProductCategory.objects.none()

    def get_serializer_context(self):
        """
        Add the request context to the serializer.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    permission_classes = [IsAuthenticated, IsShopOwner]

    def get_queryset(self):
        return Product.objects.filter(shop__owner=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()


        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date:
            queryset = queryset.filter(added_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(added_at__lte=end_date)


        min_inventory = request.query_params.get('min_inventory')
        max_inventory = request.query_params.get('max_inventory')

        if min_inventory:
            queryset = queryset.filter(inventory__gte=min_inventory)
        if max_inventory:
            queryset = queryset.filter(inventory__lte=max_inventory)


        queryset = self.filter_queryset(queryset)

        # Apply pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SaleViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer
    filterset_class = SaleFilter
    permission_classes = [IsAuthenticated, IsShopOwner]

    def get_queryset(self):
        return Sale.objects.filter(shop__owner=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        if start_date:
            queryset = queryset.filter(sale_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(sale_date__lte=end_date)


        product_price_subquery = Subquery(
            Product.objects.filter(id=OuterRef('items__product_id')).values('price')[:1]
        )
        product_mrp_subquery = Subquery(
            Product.objects.filter(id=OuterRef('items__product_id')).values('mrp')[:1]
        )

        total_profit_annotation = ExpressionWrapper(
            product_price_subquery - product_mrp_subquery,
            output_field=DecimalField()
        )

        aggregated_sales = queryset.annotate(
            total_sales=Sum(product_price_subquery * F('items__quantity')),
            total_profit=Sum(total_profit_annotation * F('items__quantity'))  # Calculate total profit
        ).values('id', 'receipt_number', 'sale_date', 'total_sales', 'total_profit')

        min_amount = request.query_params.get('min_amount', None)
        max_amount = request.query_params.get('max_amount', None)

        if min_amount is not None:
            aggregated_sales = aggregated_sales.filter(total_sales__gte=min_amount)
        if max_amount is not None:
            aggregated_sales = aggregated_sales.filter(total_sales__lte=max_amount)

        # Apply pagination
        page = self.paginate_queryset(aggregated_sales)
        if page is not None:
            return self.get_paginated_response(page)

        return Response(list(aggregated_sales))


class SaleItemViewSet(viewsets.ModelViewSet):
    serializer_class = SaleItemSerializer
    permission_classes = [IsAuthenticated, IsShopOwner]
    filterset_class = SaleItemFilter

    def get_queryset(self):
        return SaleItem.objects.filter(sale__shop__owner=self.request.user)


class ProductSoldViewSet(viewsets.ModelViewSet):
    """
    ViewSet to return total quantity and total sales value for a product sold in a given time range.
    """

    permission_classes = [IsAuthenticated, IsShopOwner]
    serializer_class = ProductSoldSerializer

    def get_queryset(self):
        """
        This method is not necessary for aggregated data, so we'll handle aggregation in the list method.
        """
        return SaleItem.objects.all()

    def list(self, request, *args, **kwargs):
        product_id = request.query_params.get('product')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not product_id:
            return Response({"error": "Product ID is required."}, status=400)

        try:
            product_id = int(product_id)
        except ValueError:
            return Response({"error": "Invalid Product ID."}, status=400)

        queryset = SaleItem.objects.filter(product_id=product_id)

        if start_date:
            queryset = queryset.filter(sale__sale_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(sale__sale_date__lte=end_date)

        product_price_subquery = Subquery(
            Product.objects.filter(id=OuterRef('product_id')).values('price')[:1]
        )

        aggregated_data = queryset.values('product_id').annotate(
            total_quantity_sold=Sum('quantity'),
            total_sales_value=Sum(F('quantity') * product_price_subquery)
        )

        if not aggregated_data:
            return Response([])

        return Response(aggregated_data)

