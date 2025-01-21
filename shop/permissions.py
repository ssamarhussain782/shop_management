from rest_framework.permissions import BasePermission

class IsShopOwner(BasePermission):
    """
    Custom permission to allow only shop owners to access their own resources.
    """

    def has_object_permission(self, request, view, obj):

        if hasattr(obj, 'shop'):
            return obj.shop.owner == request.user
        elif hasattr(obj, 'owner'):
            return obj.owner == request.user
        return False
