from rest_framework.permissions import BasePermission

class IsShopOwner(BasePermission):
    """
    Custom permission to allow only shop owners to access their own resources.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the object is tied to a shop and if the shop belongs to the user
        if hasattr(obj, 'shop'):  # If the object has a 'shop' attribute
            return obj.shop.owner == request.user  # Check if the shop belongs to the current user
        elif hasattr(obj, 'owner'):  # If the object has an 'owner' attribute (for other objects like Product)
            return obj.owner == request.user  # Ensure the owner matches the authenticated user
        return False  # Default case, permission is denied if no owner or shop attribute found
