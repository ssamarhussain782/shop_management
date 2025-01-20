from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShopViewSet, ProductCategoryViewSet, ProductViewSet, SaleViewSet, SaleItemViewSet, ProductSoldViewSet

router = DefaultRouter()

# Register viewsets with explicit basename
router.register(r'shops', ShopViewSet, basename='shop')
router.register(r'product-categories', ProductCategoryViewSet, basename='productcategory')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'sales', SaleViewSet, basename='sale')
router.register(r'sale-items', SaleItemViewSet, basename='saleitem')
router.register(r'products-sold', ProductSoldViewSet, basename='productsold')

urlpatterns = [
    path('api/', include(router.urls)),  # Include all the router-generated URLs
]
